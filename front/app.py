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

# 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

def login_screen():
    st.subheader("칵테일 테스트를 시작하려면 정보를 입력해주세요")
    
    VALID_ID = "2022203011"
    VALID_NAME = "김형일"
    
    with st.form("login_form"):
        input_id = st.text_input("본인의 학번을 입력하세요")
        input_name = st.text_input("본인의 이름을 입력하세요")
        submit_btn = st.form_submit_button("테스트 시작")
        
        if submit_btn:
            if input_id.strip() == "" or input_name.strip() == "":
                st.error("학번과 이름을 모두 정확히 입력해주세요.")
            elif input_id.strip() == VALID_ID and input_name.strip() == VALID_NAME:
                st.session_state.student_id = input_id
                st.session_state.student_name = input_name
                st.session_state.logged_in = True
                st.success(f"환영합니다, {input_name}님!")
                st.rerun() 
            else:
                st.error("등록되지 않은 학번이거나 이름이 일치하지 않습니다. 다시 확인해주세요.")

def quiz_screen():
    st.write("---")
    
    # 문항이 끝나면 결과 화면으로 이동
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
    st.subheader(f"🎉 {st.session_state.student_name}님의 취향을 분석한 결과입니다!")
    
    # 3가지 답을 모두 선택했을 경우 백엔드 API에 요청 전송
    if len(st.session_state.user_answers) == 3:
        payload = {
            "base": st.session_state.user_answers[0],
            "taste": st.session_state.user_answers[1],
            "abv": st.session_state.user_answers[2]
        }
        
        # docker-compose 안에서는 서비스명('backend')으로 통신 가능
        # 포트는 backend Dockerfile에 지정한 8000번
        api_url = "http://backend:8000/recommend"
        
        try:
            # FastAPI 백엔드 호출
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
    
    # 버튼 배치를 위한 컬럼 생성
    col1, col2 = st.columns(2)
    with col1:
        if st.button("테스트 다시 하기", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.user_answers = []
            st.rerun()
    with col2:
        if st.button("로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_question = 0
            st.session_state.user_answers = []
            st.rerun()

# 메인 실행 로직
if not st.session_state.logged_in:
    login_screen()
else:
    quiz_screen()