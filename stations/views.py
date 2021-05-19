import os
import requests
import threading
import queue

from django.views import View
from django.db import transaction, IntegrityError
from django.http import JsonResponse

from stations.models import Station, StationLog


class NewStationListView(View):
    def get(self, request):
        try:
            bikelist_seoul_api_url = "http://openapi.seoul.go.kr:8088/"\
                + os.environ.get("BIKELIST_SEOUL_API_KEY") + "/json/bikeList/"

            with transaction.atomic():
                # multithreading
                output = queue.Queue()

                def load_bikelist(start, end):
                    output.put(
                        requests.get(bikelist_seoul_api_url + str(start) + "/" + str(end)).json().get("rentBikeStatus").get("row")
                    )
                
                threads = [threading.Thread(target=load_bikelist(i, i+999)) for i in range(1, 3000, 1000)]
                result = []

                for p in threads:
                    p.start()

                for p in threads:
                    p.join()

                for p in threads:
                    result.extend(output.get())
                
                station_from_db = {i.name : i for i in list(Station.objects.all())}
                log_to_create = []

                for data in result:
                    if data["stationName"] in station_from_db:
                        station = station_from_db[data["stationName"]]
                    else:
                        kakao_local_api_url = "https://dapi.kakao.com/v2/local/geo/coord2address.json?x="\
                            + data["stationLongitude"] + "&y=" + data["stationLatitude"]
                        kakao_headers = ({'authorization' : f'KakaoAK {os.environ.get("KAKAO_REST_API_KEY")}'})
                        kakao_response = requests.get(kakao_local_api_url, headers=kakao_headers).json()
                        
                        if kakao_response["documents"]:
                            address = kakao_response["documents"][0]["address"]["address_name"]
                        else:
                            address = None

                        Station.objects.create(
                            code = data["stationId"][3:],
                            name = data["stationName"],
                            lot_address = address,
                            latitude = data["stationLatitude"],
                            longitude = data["stationLongitude"],
                            rack_cnt = data["rackTotCnt"],
                        )

                        station = Station.objects.latest("id")

                    log_to_create.append(StationLog(
                        total_cnt = data["parkingBikeTotCnt"],
                        station = station
                    ))
                
                StationLog.objects.bulk_create(log_to_create)

            return JsonResponse({'message':"SUCCESS"}, status=200)
        
        except AttributeError:
            return JsonResponse({'message':"NO_BIKELIST_DATA"}, status=400)

        except KeyError:
            return JsonResponse({'message':"API_STRUCTURE_CHANGED"}, status=400)

        except IntegrityError:
            return JsonResponse({'message':"TRANSACTION_BROKEN"}, status=500)
