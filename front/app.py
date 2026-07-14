import streamlit as st
import requests

# 페이지 설정
st.set_page_config(page_title="칵테일 취향 테스트", page_icon="🍸")

st.title("🍸 나만의 칵테일 취향 테스트")
st.markdown("**학번:** 2022203011 | **이름:** 김형일")
st.write("---")

base_options = {
    "진(Gin)": "Gin",
    "보드카(Vodka)": "Vodka",
    "럼(Rum)": "Rum",
    "데킬라(Tequila)": "Tequila",
    "위스키(Whiskey)": "Whiskey"
}

taste_options = {
    "달콤한 스위트": "Sweet", 
    "새콤한 사워": "Sour", 
    "쌉싸름한 드라이": "Dry"
}

abv_options = {
    "가볍게 (LV1)": "LV1", 
    "적당한 취기 (LV2)": "LV2", 
    "확실한 독함 (LV3)": "LV3", 
    "완전히 취하고 싶을 때 (LV4)": "LV4"
}

st.subheader("당신의 취향을 선택해주세요!")

selected_base_label = st.radio(
    "**Q1. 선호하거나 도전해보고 싶은 메인 술(기주)은?**",
    options=list(base_options.keys()),
    horizontal=True 
)

selected_taste_label = st.select_slider(
    "**Q2. 혀끝에서 느껴지는 맛 중 가장 끌리는 것은?**",
    options=list(taste_options.keys())
)

selected_abv_label = st.select_slider(
    "**Q3. 오늘 원하는 알코올 도수의 강도는?**",
    options=list(abv_options.keys())
)

st.write("---")

if st.button("🍸 내 취향에 맞는 칵테일 추천받기", use_container_width=True):
  
    payload = {
        "base": base_options[selected_base_label],
        "taste": taste_options[selected_taste_label],
        "abv": abv_options[selected_abv_label]
    }
    
    api_url = "http://backend:8000/recommend"
    
    try:
        with st.spinner('당신에게 딱 맞는 칵테일을 찾는 중입니다...'):
            response = requests.post(api_url, json=payload)
            
        if response.status_code == 200:
            result = response.json()
            st.success("🎉 취향 분석이 완료되었습니다!")
            st.markdown(f"### 🍹 추천 칵테일: **{result['name']}**")
            st.info(result['desc'])
        else:
            st.error("백엔드 서버에서 결과를 가져오는 중 문제가 발생했습니다.")
            
    except requests.exceptions.RequestException:
        st.error("백엔드 서버에 연결할 수 없습니다. 도커(백엔드) 상태를 확인해주세요.")