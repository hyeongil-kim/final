import streamlit as st
import requests

st.set_page_config(page_title="칵테일 취향 테스트")

st.title("🍸 나만의 칵테일 취향 테스트")
st.markdown("**학번:** 2022203011 | **이름:** 김형일")

@st.cache_data
def load_quiz_questions():
    questions = [
        {
            "id": 1,
            "key": "base",
            "text": "Q1. 선호하거나 도전해보고 싶은 메인 술(기주)은?",
            "choices": {
                "깔끔함의 정석 '진(Gin)'": "Gin",
                "무색, 무취, 무미의 깔끔함 '보드카(Vodka)'": "Vodka",
                "달콤한 사탕수수 풍미 '럼(Rum)'": "Rum",
                "멕시코의 정열 '데킬라(Tequila)'": "Tequila",
                "오크통 풍미의 '위스키(Whiskey)'": "Whiskey",
            }
        },
        {
            "id": 2,
            "key": "taste",
            "text": "Q2. 혀끝에서 느껴지는 맛 중 가장 끌리는 것은?",
            "choices": {
                "달콤하고 대중적인 맛 '스위트'": "Sweet", 
                "새콤하고 청량한 맛 '사워'": "Sour", 
                "쌉싸름하고 깔끔한 맛 '드라이'": "Dry"
            }
        },
        {
            "id": 3,
            "key": "abv",
            "text": "Q3. 오늘 원하는 알코올 도수의 강도는?",
            "choices": {
                "음료수처럼 가볍게 (15% 이하)": "LV1", 
                "기분 좋은 적당한 취기 (15~25%)": "LV2", 
                "도수가 확실히 느껴지는 독함 (25~40%)": "LV3", 
                "오늘 밤 완전히 취하고 싶을 때 (40% 이상)": "LV4"
            }
        }
    ]
    return questions

questions = load_quiz_questions()

if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []

def quiz_screen():
    st.write("---")
    
    if st.session_state.current_question >= len(questions):
        show_result()
        return

    q = questions[st.session_state.current_question]
    
    progress = st.session_state.current_question / len(questions)
    st.progress(progress)
    st.write(f"**Q{q['id']}. {q['text']}**")
    
    for choice_text, choice_value in q['choices'].items():
        if st.button(choice_text, use_container_width=True):
            st.session_state.user_answers.append(choice_value)
            st.session_state.current_question += 1
            st.rerun()

def show_result():
    st.subheader("🎉 당신의 취향을 분석한 결과입니다!")
    
    if len(st.session_state.user_answers) == 3:
        payload = {
            "base": st.session_state.user_answers[0],
            "taste": st.session_state.user_answers[1],
            "abv": st.session_state.user_answers[2]
        }
     
        api_url = "http://backend:8000/recommend"
        
        try:
            response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                st.markdown(f"### 추천 칵테일: **{result['name']}**")
                st.info(result['desc'])
            else:
                st.error("백엔드 서버에서 결과를 가져오는 중 문제가 발생했습니다.")
                
        except requests.exceptions.RequestException as e:
            st.error("백엔드 서버에 연결할 수 없습니다. 서버 상태를 확인해주세요.")
    else:
        st.warning("선택된 답변 정보가 부족합니다. 처음부터 다시 시도해주세요.")
    
    st.write("---")
    
    if st.button("테스트 다시 하기", use_container_width=True):
        st.session_state.current_question = 0
        st.session_state.user_answers = []
        st.rerun()

quiz_screen()