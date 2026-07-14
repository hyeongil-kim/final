from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI(title="칵테일 추천 API")

# 프론트엔드에서 넘어올 데이터 모델 정의
class CocktailRequest(BaseModel):
    base: str
    taste: str
    abv: str

# 기존 app.py에 있던 results 딕셔너리를 백엔드로 이동
results_data = {
    "Gin_Sweet_LV1": {"name": "싱가포르 슬링 (Singapore Sling)", "desc": "체리 브랜디와 과일 주스가 진과 어우러져 화려하고 달콤한 풍미를 자랑하는 가벼운 칵테일입니다."},
    "Gin_Sweet_LV2": {"name": "톰 콜린스 (Tom Collins)", "desc": "레몬주스와 설탕에 탄산수를 더해 청량하면서도 달콤하게 즐기는 대중적인 칵테일입니다."},
    "Gin_Sweet_LV3": {"name": "비즈 니즈 (Bee's Knees)", "desc": "진에 꿀과 레몬의 진한 단맛을 더해 부드러운 목넘김과 높은 도수를 동시에 만족시킵니다."},
    "Gin_Sweet_LV4": {"name": "마티니 슬링 (Martini Sling)", "desc": "강렬한 진의 도수 속에 스위트 베르무트의 달콤함을 숨겨 깊은 취기를 선사하는 고도수 술입니다."},
    "Gin_Sour_LV1": {"name": "진 피즈 (Gin Fizz)", "desc": "레몬의 상큼함과 진의 깔끔함이 탄산과 만나 가볍고 새콤하게 마시기 좋은 저도수 칵테일입니다."},
    "Gin_Sour_LV2": {"name": "김렛 (Gimlet)", "desc": "진과 라임 주스의 황금 비율! 새콤하고 군더더기 없는 맛으로 사랑받는 정석 칵테일입니다."},
    "Gin_Sour_LV3": {"name": "화이트 레이디 (White Lady)", "desc": "오렌지 리큐어와 레몬즙을 흔들어 만들어, 짜릿한 상큼함 뒤에 높은 도수가 찾아옵니다."},
    "Gin_Sour_LV4": {"name": "롱아일랜드 아이스티 (Gin Base)", "desc": "다양한 독주가 섞여 새콤달콤하지만, 마시다 보면 순식간에 취하는 칵테일의 대명사입니다."},
    "Gin_Dry_LV1": {"name": "진토닉 (Gin & Tonic)", "desc": "단맛 없이 진의 솔잎 향과 토닉워터의 청량함이 어우러진 가장 깔끔한 저도수 칵테일입니다."},
    "Gin_Dry_LV2": {"name": "네그로니 (Negroni)", "desc": "진의 드라이함에 캄파리의 쌉싸름함이 매력적으로 다가오는 어른들을 위한 중도수 칵테일입니다."},
    "Gin_Dry_LV3": {"name": "드라이 마티니 (Dry Martini)", "desc": "'칵테일의 왕'. 단맛이 전혀 없고 진 본연의 날카롭고 묵직한 맛을 극대화한 독한 술입니다."},
    "Gin_Dry_LV4": {"name": "베스퍼 마티니 (Vesper Martini)", "desc": "영화 007 우아한 독주. 진과 보드카가 섞여 상상 이상의 드라이함과 고도수를 선사합니다."},
    
    "Vodka_Sweet_LV1": {"name": "섹스 온 더 비치 (Sex on the Beach)", "desc": "복숭아, 크랜베리, 오렌지가 섞여 과일 주스처럼 달콤하고 가볍게 즐기는 트로피컬 맛입니다."},
    "Vodka_Sweet_LV2": {"name": "모스코 뮬 (Moscow Mule)", "desc": "진저에일의 알싸한 달콤함과 라임 향이 어우러져 청량하면서도 기분 좋은 취기를 줍니다."},
    "Vodka_Sweet_LV3": {"name": "블랙 러시안 (Black Russian)", "desc": "보드카에 진하고 달콤한 커피 리큐어가 더해져 디저트처럼 달달하고 묵직하게 즐기는 술입니다."},
    "Vodka_Sweet_LV4": {"name": "에스프레소 마티니 (Espresso Martini)", "desc": "에스프레소의 커피 향과 보드카의 강렬함이 만나 정신을 깨우는 독하고 달콤한 고도수 칵테일입니다."},
    "Vodka_Sour_LV1": {"name": "보드카 크랜베리 (Vodka Cranberry)", "desc": "붉은 크랜베리 주스의 새콤함이 가볍고 부담 없이 상큼한 목넘김을 제공하는 저도수 칵테일입니다."},
    "Vodka_Sour_LV2": {"name": "코스모폴리탄 (Cosmopolitan)", "desc": "라임과 크랜베리의 세련된 새콤함이 보드카와 깔끔하게 매칭된 도시적인 중도수 칵테일입니다."},
    "Vodka_Sour_LV3": {"name": "레몬 드롭 마티니 (Lemon Drop)", "desc": "레몬의 짜릿한 신맛과 설탕 리큐어가 만나 상큼하지만 은근히 독한 반전 매력의 마티니입니다."},
    "Vodka_Sour_LV4": {"name": "카미카제 (Kamikaze)", "desc": "입안을 찌르는 듯한 라임의 강렬한 신맛과 보드카 본연의 높은 도수가 만난 독한 술입니다."},
    "Vodka_Dry_LV1": {"name": "보드카 토닉 (Vodka Tonic)", "desc": "보드카 특유의 깔끔함에 토닉워터의 탄산만 가미되어 군더더기 없이 시원한 저도수 칵테일입니다."},
    "Vodka_Dry_LV2": {"name": "보드카 소다 (Vodka Soda)", "desc": "단맛을 완벽히 배제하고 탄산수와 레몬 휠만 띄워 극강의 깔끔함을 자랑하는 중도수 술입니다."},
    "Vodka_Dry_LV3": {"name": "보드카 마티니 (Vodka Martini)", "desc": "풀 향 대신 오직 에탄올의 순수하고 드라이한 맛을 깊고 묵직하게 즐기는 정통 독주 칵테일입니다."},
    "Vodka_Dry_LV4": {"name": "보드카 온더락 (Vodka on the Rocks)", "desc": "프리미엄 보드카 본연의 드라이하고 차가운 알코올 감각을 온전히 온몸으로 느끼는 방식입니다."},

    "Rum_Sweet_LV1": {"name": "피냐 콜라다 (Pina Colada)", "desc": "달콤한 파인애플과 부드러운 코코넛 크림이 섞여 달달하고 밀키한 휴양지 느낌의 칵테일입니다."},
    "Rum_Sweet_LV2": {"name": "쿠바 리브레 (Cuba Libre)", "desc": "화이트 럼에 콜라와 라임을 섞어 청량하고 달콤하게 누구나 즐기기 좋은 대중적인 술입니다."},
    "Rum_Sweet_LV3": {"name": "다크 앤 스토미 (Dark 'n' Stormy)", "desc": "다크 럼의 묵직한 사탕수수 향과 진저비어의 알싸한 단맛이 매력적인 묵직한 취기의 술입니다."},
    "Rum_Sweet_LV4": {"name": "파우스트 (Faust)", "desc": "오버프루프 독주에 단맛을 더해, 달콤한 첫맛 뒤에 목이 타는 듯한 강력한 고도수를 선사합니다."},
    "Rum_Sour_LV1": {"name": "모히토 (Mojito)", "desc": "라임과 신선한 애플민트, 탄산수가 어우러져 청량함과 새콤함이 폭발하는 대중적인 저도수 칵테일입니다."},
    "Rum_Sour_LV2": {"name": "다이키리 (Daiquiri)", "desc": "럼, 라임, 설탕 딱 세 가지로 럼 고유의 풍미와 새콤한 신맛의 황금 밸런스를 보여줍니다."},
    "Rum_Sour_LV3": {"name": "바카디 칵테일 (Bacardi Cocktail)", "desc": "석류 시럽의 예쁜 빛깔과 라임의 새콤함이 조화를 이루는 은근히 독한 클래식 쇼트 드링크입니다."},
    "Rum_Sour_LV4": {"name": "좀비 (Zombie)", "desc": "강력한 럼 여러 종과 과일 주스를 섞어 맛은 새콤달콤하지만 내일 아침을 보장할 수 없는 고도수 술입니다."},
    "Rum_Dry_LV1": {"name": "럼 토닉 (Rum Tonic)", "desc": "화이트 럼에 토닉워터를 더해 은은한 사탕수수 풍미만 남기고 드라이하게 마무리한 청량한 잔입니다."},
    "Rum_Dry_LV2": {"name": "엘 프레시덴테 (El Presidente)", "desc": "럼과 드라이 베르무트의 조합으로, 달지 않고 깔끔한 오렌지 향이 스치는 세련된 스타일입니다."},
    "Rum_Dry_LV3": {"name": "마이타이 드라이 (Mai Tai Dry)", "desc": "단맛을 극도로 줄이고 럼 고유의 드라이하고 깊은 나무 향을 살려 독하게 빌드한 칵테일입니다."},
    "Rum_Dry_LV4": {"name": "네이비 스트렝스 럼 샷 (Navy Strength Rum)", "desc": "어떠한 희석도 없이 독주 고유의 사탕수수 향과 거친 알코올감을 드라이하게 마시는 최고도수 선택입니다."},

    "Tequila_Sweet_LV1": {"name": "데킬라 선라이즈 (Tequila Sunrise)", "desc": "오렌지 주스와 석류 시럽을 넣어 일출을 형상화한 달콤하고 가벼운 데킬라 입문용 술입니다."},
    "Tequila_Sweet_LV2": {"name": "엘 디아블로 (El Diablo)", "desc": "카시스 리큐어의 베리 향 단맛과 진저에일이 만나 매혹적인 루비 빛 단맛을 내는 칵테일입니다."},
    "Tequila_Sweet_LV3": {"name": "멕시칸 뮬 (Mexican Mule)", "desc": "데킬라 특유의 선인장 향과 진저비어의 단맛이 만나 묵직한 타격감과 당도를 함께 채워줍니다."},
    "Tequila_Sweet_LV4": {"name": "아가베 골드 샷 (Agave Gold)", "desc": "숙성된 골드 데킬라의 진한 아가베 풍미와 강렬한 알코올 도수를 온전히 달콤하게 음미하는 조합입니다."},
    "Tequila_Sour_LV1": {"name": "팔로마 (Paloma)", "desc": "자몽 소다와 라임을 더해 상큼하고 쌉싸름하게 톡 쏘는 청량 지수 100%의 저도수 칵테일입니다."},
    "Tequila_Sour_LV2": {"name": "마가리타 (Margarita)", "desc": "데킬라, 라임, 잔 테두리의 소금이 만나 신맛과 짠맛의 완벽한 앙상블을 이루는 칵테일의 정석입니다."},
    "Tequila_Sour_LV3": {"name": "토미스 마가리타 (Tommy's Margarita)", "desc": "인공 시럽 대신 생라임즙을 극대화하여 데킬라 본연의 향과 짜릿한 신맛을 독하게 즐기는 버전입니다."},
    "Tequila_Sour_LV4": {"name": "마가리타 스트롱 (Margarita Strong)", "desc": "얼음을 최소화하고 원액 비율을 높여 짜릿한 신맛 뒤에 거대한 알코올감이 몰려오는 독한 한 잔입니다."},
    "Tequila_Dry_LV1": {"name": "데킬라 토닉 (Tequila Tonic)", "desc": "데킬라에 단맛 없는 토닉워터와 라임을 곁들여 깔끔하고 산뜻하게 기분 내기 좋은 드라이 칵테일입니다."},
    "Tequila_Dry_LV2": {"name": "바탕가 (Batanga)", "desc": "콜라를 섞되 소금을 첨가해 단맛을 잡아 드라이하고 짭조름하게 마시는 맥시코 현지 스타일입니다."},
    "Tequila_Dry_LV3": {"name": "데킬라 안제호 온더락 (Anejo Rocks)", "desc": "오크통에 장기 숙성된 프리미엄 데킬라의 드라이함과 나무 향을 얼음과 함께 천천히 음미하는 독주입니다."},
    "Tequila_Dry_LV4": {"name": "데킬라 스트레이트 (Tequila Shot)", "desc": "라임과 레몬 한 조각을 베어 물며 데킬라 고유의 야성적인 드라이함을 원샷으로 느끼는 최고도수 방식입니다."},

    "Whiskey_Sweet_LV1": {"name": "아일리시 콕 (Irish Coke)", "desc": "부드러운 아일리시 위스키에 콜라를 섞어 입문자도 달달하고 편안하게 접근 가능한 저도수 술입니다."},
    "Whiskey_Sweet_LV2": {"name": "잭 콕 (Jack & Coke)", "desc": "버번 테네시 위스키 특유의 스모키함과 콜라의 달콤함이 만나 전 세계적인 대중성을 확보한 칵테일입니다."},
    "Whiskey_Sweet_LV3": {"name": "올드 패션드 (Old Fashioned)", "desc": "설탕과 비터스를 녹여 위스키의 오크 향을 묵직하고 달콤 쌉싸름하게 받쳐주는 중후한 칵테일입니다."},
    "Whiskey_Sweet_LV4": {"name": "갓파더 (Godfather)", "desc": "위스키와 달콤한 아몬드 리큐어를 섞어 영화 대부처럼 묵직하고 중후한 단맛을 품은 최고도수 독주입니다."},
    "Whiskey_Sour_LV1": {"name": "린치버그 레모네이드 (Lynchburg Lemonade)", "desc": "위스키에 레몬과 사이다를 스티어하여 상큼하고 청량하게 에이드처럼 마시는 저도수 하이볼입니다."},
    "Whiskey_Sour_LV2": {"name": "위스키 사워 (Whiskey Sour)", "desc": "위스키 풍미에 레몬즙의 새콤함이 어우러져 부드러우면서도 상큼한 맛을 내는 정통 칵테일입니다."},
    "Whiskey_Sour_LV3": {"name": "뉴욕 (New York Cocktail)", "desc": "위스키와 레몬, 석류 시럽이 만나 노을빛 색감과 함께 새콤하고 묵직한 타격감을 뽐냅니다."},
    "Whiskey_Sour_LV4": {"name": "불레바디에 사워 (Boulevardier Sour)", "desc": "버번의 묵직한 도수에 쌉싸름함과 레몬의 강렬한 신맛을 한 번에 우려낸 초고도수 변형 칵테일입니다."},
    "Whiskey_Dry_LV1": {"name": "위스키 하이볼 (Whiskey Highball)", "desc": "위스키에 단맛 없는 탄산수와 레몬만 더해 식사와 함께 깔끔하고 드라이하게 즐기는 깔끔한 하이볼입니다."},
    "Whiskey_Dry_LV2": {"name": "민트 줄렙 (Mint Julep)", "desc": "버번 위스키에 신선한 민트의 시원함을 가미하여 드라이하고 청량하게 마시는 정통 미국식 칵테일입니다."},
    "Whiskey_Dry_LV3": {"name": "맨해튼 (Manhattan)", "desc": "'칵테일의 여왕'. 위스키 고유의 드라이함과 허브 향이 조화된 깊고 진한 정통 클래식 독주입니다."},
    "Whiskey_Dry_LV4": {"name": "싱글몰트 스트레이트 (Single Malt)", "desc": "첨가물 없이 위스키 오크통 본연의 드라이함과 깊은 피트 풍미를 그대로 목구멍으로 넘기는 방식입니다."}
}

@app.post("/recommend")
def recommend_cocktail(req: CocktailRequest):
    final_type = f"{req.base}_{req.taste}_{req.abv}"
    # 조합이 일치하지 않을 때를 대비한 기본값
    result = results_data.get(final_type, {"name": "미스터리 칵테일", "desc": "아직 준비되지 않은 조합입니다. 다시 한번 테스트 해주세요."})
    return result