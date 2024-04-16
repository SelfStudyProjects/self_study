
|                                          이혜림(팀장)                                           |                                           이규성                                           |                                           전지용                                           |                                           정진영                                           |                                           박경민                                           |
| :---------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------: |
| <img src="https://discordapp.com/channels/1172400071397101629/1222471136982601758/1229662398244196474" width="200" height="200"> | <img src="https://discordapp.com/channels/1172400071397101629/1222471136982601758/1229662653270720612" width="200" height="200"> | <img src="지용님 개인 프로필 사진 링크" width="200" height="200"> | <img src="진영님 개인 프로필 사진 링크" width="200" height="200"> | <img src="경민님 개인 프로필 사진 링크" width="200" height="200"> |
|                   <a href="https://github.com/matty255"> 🌱 HY. Lee                    |                      <a href="https://github.com/rkawkclzls"> 🌱 rkawkclzls                      |              <a href="https://github.com/mkdirlife"> 🌱 mkdirlife              |                  <a href="https://github.com/najasinis"> 🌱 najasinis                  |                     <a href="https://github.com/Masterdual"> 🌱 Masterdual                     |
|                   프로젝트의 아키텍처를 설계하고, 기획 단계에서 요구사항을 명확히 정의하며, 프론트엔드 개발을 담당 했습니다.                    |                      AI 모델의 출력값(이미지)을 저장하고 관리하는 미디어 앱을 작성하여 분석 결과를 효과적으로 활용할 수 있도록 했습니다.                      |              utils 앱 개발을 담당하고 있습니다. 다른 애플리케이션에서 공통적으로 사용할 수 있는 기능을 제공했습니다.              |                  accounts 앱 및 chat 앱 개발을 담당하고 있으며, 모델링을 분담하고 있습니다. 더불어 사용자 인증과 관련된 기능들(정보 관리, 권한 부여 등), 채팅방 생성 기능, 실시간 채팅 기능들을 구현했습니다.                  |                     alarm 앱 개발을 담당했습니다. 적절한 경고 메시지를 커스텀하고, DB에 저장할 수 있도록 했습니다.                     |

accounts
Swagger

URL	HTTP<br>Method	비고	로그인<br>권한	작성자<br>권한	Admin<br>권한
/api/accounts/login/	POST	유저 로그인			
/api/accounts/logout/	POST	유저 로그아웃	✔		
/api/accounts/register-admin/	POST	관리자 계정 생성			✔
/api/accounts/register/	POST	일반 사용자 계정 생성			
/api/accounts/user/	GET	현재 로그인한 사용자 정보 조회	✔		
/api/accounts/users/	GET	전체 사용자 목록 조회			✔
/api/accounts/<int:pk>/	GET	특정 사용자 정보 조회			✔
/api/accounts/<int:pk>/	PUT	특정 사용자 정보 수정		✔	✔
/api/accounts/<int:pk>/	PATCH	특정 사용자 정보 부분 수정		✔	✔
/api/accounts/<int:pk>/	DELETE	특정 사용자 삭제			✔
/api/accounts/<int:pk>/delete/	DELETE	특정 사용자 삭제			✔
/api/accounts/<int:pk>/tokens/generate/	POST	특정 사용자 토큰 생성			✔

# 🏠 SELF_STUDY
> 본 페이지 방문하시는 모든 분들의 욕망-비전-목표가 결국 이루어지길!

안녕하세요!

개인적으로 제가 개발 공부한 것들을 기록하였습니다. :D

모두들 귀한 걸음 감사해요!

## ✨  공부 연혁 
2022 ~ : 코드잇 독학 (HTML/CSS, JS, 컴퓨터 구조, 머신러닝, 피그마)

2023 ~ : 유튜브 독학(with 조코딩, 노마드코더, 얄팍한 코딩사전(얄코) 등)

2023.12 : 모두의 연구소 X 제주 오름캠프 AI 활용 백엔드 과정 참여

## ✨  (현재) 공부 언어
파이썬(Django)

HTML/CSS/JS

자바

AWS 배포(Ubuntu)

## ✨ 목적
공부 기록 및 개발 포트폴리오 기록

## ✨ 개발 프로젝트 연혁
2023.03 ~ 06 : 맞춤형 수제 펫푸드 추천 서비스, 힐링펫츠 서비스 BM팀 대표(PM 겸겸직, UML 작성)
2023.09 ~ 12 : 미라클플레이 백엔드 파트 역임(db 설계서)
