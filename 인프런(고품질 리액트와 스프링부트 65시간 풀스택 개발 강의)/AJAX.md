# JavaScript Fetch API와 AJAX 핵심 개념 정리

## 1. JavaScript Fetch API란?

**Fetch API**는 JavaScript에서 서버와 데이터를 주고받기 위한 현대적인 방법입니다. 기존의 XMLHttpRequest를 대체하는 더 간단하고 직관적인 API로, Promise 기반으로 동작합니다.

### 기본 구조
```javascript
fetch('API_URL')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## 2. 데이터 형태별 처리 방법

### JSON 데이터 처리
- **response.json()**: JSON 형태의 응답을 JavaScript 객체로 변환
- 서버에서 JSON으로 데이터를 보내면 프론트엔드에서 이를 파싱하여 사용

### 일반 텍스트 처리
- **response.text()**: 일반 텍스트 형태의 응답 처리

## 3. HTTP 메소드별 활용

### GET 요청 (데이터 조회)
```javascript
fetch('/api/data')
  .then(response => response.json())
  .then(data => console.log(data));
```

### POST 요청 (데이터 생성)
```javascript
fetch('/api/data', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(데이터객체)
})
```

### PUT/DELETE 요청
- **PUT**: 데이터 수정
- **DELETE**: 데이터 삭제

## 4. CRUD 연산과의 연관성

- **Create**: POST 메소드 사용
- **Read**: GET 메소드 사용  
- **Update**: PUT 메소드 사용
- **Delete**: DELETE 메소드 사용

## 5. 실무에서의 활용 포인트

### 프론트엔드-백엔드 통신
- 프론트엔드에서 JavaScript 언어로 개발하고 백엔드 영역에서는 서버 API를 통해 데이터 주고받기
- 데이터를 프론트엔드 영역에서 백엔드 영역으로 데이터를 주고받을 때 새로 데이터를 프론트엔드에서 사용하는 함수 기능

### 비동기 처리의 중요성
- fetch 함수는 비동기로 동작하여 서버 응답을 기다리는 동안 다른 작업 수행 가능
- Promise 체인을 통해 순차적으로 데이터 처리

## 6. jQuery Ajax와의 비교

### jQuery Ajax의 특징
- jQuery 라이브러리 안에 있는 ajax는 지금도 널리 사용
- 현재 웹계에서 유일하게 우리나라에서만 SI업체의 90% 이상이 jQuery의 AJAX 사용

### Fetch API의 장점
- 별도 라이브러리 없이 브라우저 내장 기능 사용
- Promise 기반으로 더 현대적이고 직관적인 코드 작성
- 더 가볍고 성능이 우수

## 7. 실제 개발 시 주의사항

### 에러 처리
```javascript
fetch('/api/data')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .catch(error => console.error('Error:', error));
```

### CORS 이슈
- 다른 도메인의 API를 호출할 때 CORS(Cross-Origin Resource Sharing) 정책 확인 필요
- 개발 환경에서는 localhost:8080 등의 포트 설정 중요

### 데이터 검증
- 서버로부터 받은 데이터가 예상한 형태인지 확인
- undefined나 null 값에 대한 적절한 처리 필요

## 8. 현업에서의 트렌드

- **Fetch API**: 모던 웹 개발에서 표준으로 사용
- **jQuery Ajax**: 레거시 시스템이나 기존 프로젝트에서 여전히 활용
- 프로젝트 시간에 따라 적절한 기술 선택이 중요하며, 더 좋은 성과를 위해 상황에 맞는 방향성 채택