from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Drug
from io import BytesIO
from PIL import Image
from accounts.models import User
from rest_framework.generics import get_object_or_404
import glob
from bs4 import BeautifulSoup
import requests
import os
from urllib.request import urlretrieve
from .serializers import DrugCreateSerializer
from roboflow import Roboflow
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By

rf = Roboflow(api_key="yIvjhxReJhbmoou26jEh")
project = rf.workspace().project("medicine-fp06v")
model = project.version(1).model


# Create your views here.


class DrugCreateView(APIView):
    def post(self, request):
        print(request.data["img"])
        uploaded_img = request.data["img"]
        if not uploaded_img:
            return Response({"error": "이미지가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        img_data = uploaded_img.read()
        image = Image.open(BytesIO(img_data))
        image = np.array(image)

        cv2.imwrite("./media/UploadDrug/pill.jpg", image)
        img = "./media/UploadDrug/pill.jpg"
        print(img)

        # 이미지 파일 목록을 취득(패스)
        pics = glob.glob(img)

        # 조정 후 사이즈를 지정(베이스 이미지)
        size = (960, 960)
        # 리사이즈 처리
        for pic in pics:
            base_pic = np.zeros((size[1], size[0], 3), np.uint8)
            pic1 = cv2.imread(pic, cv2.IMREAD_COLOR)
            h, w = pic1.shape[:2]
            ash = size[1] / h
            asw = size[0] / w
            # 크기 비율 맞추기
            if asw < ash:
                sizeas = (int(w * asw), int(h * asw))
            else:
                sizeas = (int(w * ash), int(h * ash))
            # 비율 맞춰 줄인 사진
            pic1 = cv2.resize(pic1, dsize=sizeas)
            base_pic[
                int(size[1] / 2 - sizeas[1] / 2) : int(size[1] / 2 + sizeas[1] / 2),
                int(size[0] / 2 - sizeas[0] / 2) : int(size[0] / 2 + sizeas[0] / 2),
                :,
            ] = pic1
            # print(base_pic.shape)
            cv2.imwrite("./media/" + pic, base_pic)

        # infer on a local image
        response = model.predict(pic, confidence=40, overlap=30).json()
        # print(response)

        # 검색 결과가 존재할 시 응답을 selenium 으로 검색하여 정보 저장
        if response["predictions"]:
            drug_name = response["predictions"][0]["class"]
            driver = webdriver.Chrome()
            url = "https://terms.naver.com/"
            driver.get(url)

            driver.find_element(By.CLASS_NAME, ("search_input")).send_keys(
                f"{drug_name}"
            )
            driver.find_element(
                By.XPATH, '//*[@id="terms_search_form"]/fieldset/div/input[1]'
            ).click()

            driver.find_element(
                By.XPATH, '//*[@id="content"]/div[2]/ul/li/div[2]/div[1]/strong/a'
            ).click()

            url = driver.current_url
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
            }
            data = requests.get(url, headers=headers)

            soup = BeautifulSoup(data.text, "html.parser")

            drug_img = soup.find("img", attrs={"class": ""}).get("src")
            print(drug_img)
            # drug_img = drug_img_box.attrs["src"]
            drug_form = (
                soup.select_one(
                    "#size_ct > div.att_type > div > div.wr_tmp_profile > div > table > tbody > tr:nth-child(8) > td"
                )
                .get_text()
                .strip()
            )
            drug_company = (
                soup.select_one(
                    "#size_ct > div.att_type > div > div.wr_tmp_profile > div > table > tbody > tr:nth-child(3) > td"
                )
                .get_text()
                .strip()
            )
            drug_ingre = soup.select_one("p.txt:nth-child(6)").get_text()

            # 효능 / 효과
            drug_eff = soup.select_one("p.txt:nth-child(10)").get_text()

            drug_data = {
                "name": drug_name,
                "company": drug_company,
                "drug_image": drug_img,
                "form": drug_form,
                "ingredient": drug_ingre,
            }
            print(drug_data)

            try:
                Drug.objects.get(name=drug_name)
                return Response({"message": "이미 등록된 알약입니다."}, status=status.HTTP_200_OK)
            except:
                Drug.objects.create(
                    name=drug_data["name"],
                    company=drug_data["company"],
                    drug_image=drug_data["drug_image"],
                    form=drug_data["form"],
                    ingredient=drug_data["ingredient"],
                )
                return Response({"message": "등록 완료"}, status=status.HTTP_201_CREATED)

        else:
            return Response(
                {"error": "인식할 수 없습니다. 정보를 직접 입력해주세요"},
                status=status.HTTP_400_BAD_REQUEST,
            )
