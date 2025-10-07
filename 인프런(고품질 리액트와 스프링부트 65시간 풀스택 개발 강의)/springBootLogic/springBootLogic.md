알겠어! 정말 수고했어. 지금부터 신입 백엔드 개발자가 **실무에서 반드시 알아야 하는** Spring Boot 프로젝트 구조와 핵심 개념들을 체계적으로 정리해줄게.

---

# 📚 Spring Boot 프로젝트 완벽 가이드 (신입 백엔드 개발자용)

## 🎯 Chapter 1: 프로젝트 기본 구조 이해하기

### 1.1 Spring Boot란?
- **정의**: 백엔드 영역을 개발하는 Java 기반 프레임워크
- **역할**: 웹 애플리케이션의 서버 측 로직을 처리
- **특징**: 
  - 설정이 간편함 (Convention over Configuration)
  - 내장 서버(Tomcat) 포함
  - 의존성 관리가 쉬움

### 1.2 프로젝트 vs 프로그램
- **프로젝트**: 여러 프로그램을 구성하는 환경적 파일
- **프로그램**: 실행 가능한 코드 파일
- **Spring Boot 프레임워크**: 프로그램을 설정하는 환경적 프레임워크

---

## 📁 Chapter 2: 폴더 구조의 원리 (필수 암기!)

### 2.1 최상위 구조
```
프로젝트 루트/
├── src/
│   ├── main/
│   │   ├── java/           # Java 소스 코드
│   │   └── resources/      # 설정 파일, 정적 리소스
│   └── test/              # 테스트 코드
├── build.gradle (또는 pom.xml)  # 빌드 설정
└── application.properties  # 환경 설정
```

### 2.2 src/main/java 구조 (MVC 패턴 기반)
```
com.example.project/
├── Application.java        # 메인 실행 파일 ⭐
├── config/                # 설정 클래스
│   ├── SecurityConfig.java
│   └── CorsConfig.java
├── controller/            # Controller (C)
├── service/              # Business Logic
├── repository/           # Data Access (Model의 일부)
├── entity/               # Database Model (M)
├── dto/                  # Data Transfer Object
└── util/                 # 유틸리티 (JWT 등)
```

---

## 🔥 Chapter 3: 핵심 개념 - MVC 패턴 (실무 필수!)

### 3.1 MVC란?
- **Model**: 데이터와 비즈니스 로직 (Entity, Repository)
- **View**: 사용자 인터페이스 (Frontend - React 등)
- **Controller**: 요청 처리 및 응답 (Controller)

### 3.2 왜 MVC를 사용하나?
1. **역할 분리**: 각 계층이 독립적으로 동작
2. **유지보수 용이**: 수정 시 다른 부분에 영향 최소화
3. **협업 효율**: 프론트/백엔드 개발자가 독립적으로 작업 가능

### 3.3 Spring Boot에서의 MVC
```
Frontend (View) ← REST API → Controller ← Service ← Repository → Database (Model)
```

---

## ⚙️ Chapter 4: application.properties 설정 (실무 핵심!)

### 4.1 파일 위치
- `src/main/resources/application.properties`

### 4.2 필수 설정 항목

#### 4.2.1 서버 포트 설정
```properties
server.port=8080
```
- 기본값: 8080
- 포트 충돌 시 변경 필요

#### 4.2.2 MySQL 데이터베이스 연결 ⭐⭐⭐
```properties
# JDBC URL 설정
spring.datasource.url=jdbc:mysql://localhost:3306/데이터베이스명?useSSL=false&serverTimezone=UTC&characterEncoding=UTF-8

# 사용자 정보
spring.datasource.username=root
spring.datasource.password=비밀번호

# 드라이버 클래스 (MySQL 8.0 이상 필수)
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
```

**중요 포인트**:
- `useSSL=false`: SSL 보안 설정 (개발 환경에서는 false)
- `serverTimezone=UTC`: 서버 시간대 설정 (한국은 KRC도 가능)
- `characterEncoding=UTF-8`: 한글 인코딩

#### 4.2.3 JPA 설정 ⭐⭐⭐
```properties
# Hibernate 설정
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect
spring.jpa.hibernate.ddl-auto=update

# SQL 로그 출력 (개발 시 필수!)
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

**ddl-auto 옵션 설명** (실무 필수 지식!):
- `create`: 기존 테이블 삭제 후 새로 생성 (⚠️ 데이터 손실!)
- `create-drop`: 애플리케이션 종료 시 테이블 삭제
- `update`: 변경사항만 반영 (실무에서 가장 많이 사용)
- `validate`: 스키마 검증만 수행
- `none`: 아무것도 하지 않음

---

## 🔐 Chapter 5: Spring Security 개념 (보안 필수!)

### 5.1 Spring Security란?
- **역할**: 인증(Authentication)과 인가(Authorization) 처리
- **위치**: `config/SecurityConfig.java`

### 5.2 주요 기능
1. **로그인/로그아웃 처리**
2. **권한 관리** (ROLE_USER, ROLE_ADMIN 등)
3. **CSRF 보호**
4. **세션 관리**

### 5.3 JWT vs 세션
```
전통적 방식 (Session):
- 백엔드에 세션 저장
- 서버 메모리 사용

현대적 방식 (JWT Token):
- 프론트엔드에 토큰 저장
- Stateless (서버 부담 감소)
```

### 5.4 실무에서 꼭 알아야 할 점
- **JWT 구조**: Header.Payload.Signature
- **유효 시간**: Access Token (짧게), Refresh Token (길게)
- **보안**: 민감한 정보는 JWT에 저장하지 않음!

---

## 🌐 Chapter 6: CORS 설정 (프론트 연동 필수!)

### 6.1 CORS란?
- **Cross-Origin Resource Sharing**
- 다른 도메인 간의 리소스 공유를 허용하는 보안 정책

### 6.2 왜 필요한가?
```
Frontend (localhost:3000) ↔ Backend (localhost:8080)
```
- 기본적으로 브라우저는 다른 포트 간 통신을 차단
- CORS 설정으로 허용 필요

### 6.3 설정 방법
```java
@Configuration
public class CorsConfig {
    @Bean
    public CorsFilter corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true);
        config.addAllowedOrigin("http://localhost:3000");
        config.addAllowedHeader("*");
        config.addAllowedMethod("*");
        source.registerCorsConfiguration("/**", config);
        return new CorsFilter(source);
    }
}
```

---

## 🗄️ Chapter 7: JPA와 Hibernate (데이터베이스 핵심!)

### 7.1 JPA란?
- **Java Persistence API**
- Java 객체와 데이터베이스 테이블을 매핑하는 표준

### 7.2 Hibernate란?
- JPA의 구현체 (실제 동작하는 프레임워크)

### 7.3 왜 사용하나?
**SQL 없이 데이터베이스 조작 가능!**
```java
// SQL: SELECT * FROM user WHERE username = 'john'
userRepository.findByUsername("john");

// SQL: INSERT INTO user VALUES (...)
userRepository.save(newUser);
```

### 7.4 실무 필수 개념

#### Entity (테이블 매핑)
```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String username;
    
    @Column(nullable = false)
    private String password;
}
```

#### Repository (데이터 접근)
```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
}
```

---

## 🔧 Chapter 8: 빌드 도구 (Gradle vs Maven)

### 8.1 역할
- 의존성(Dependency) 관리
- 프로젝트 빌드 및 배포

### 8.2 build.gradle 주요 설정
```gradle
dependencies {
    // Spring Boot Starter
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-security'
    
    // MySQL Driver
    runtimeOnly 'com.mysql:mysql-connector-j'
    
    // JWT
    implementation 'io.jsonwebtoken:jjwt:0.9.1'
    
    // Lombok (코드 간소화)
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
}
```

### 8.3 실무 팁
- `implementation`: 컴파일 + 런타임에 필요
- `runtimeOnly`: 런타임에만 필요
- `compileOnly`: 컴파일에만 필요

---

## 🚀 Chapter 9: 애플리케이션 실행

### 9.1 메인 클래스
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 9.2 실행 방법
1. **IDE (Eclipse)**: Run As → Spring Boot App
2. **터미널**: `./gradlew bootRun`
3. **JAR 파일**: `java -jar application.jar`

### 9.3 포트 충돌 해결
```bash
# Windows
netstat -ano | findstr :8080
taskkill /PID [PID번호] /F

# Mac/Linux
lsof -i :8080
kill -9 [PID번호]
```

---

## 💡 Chapter 10: 실무 필수 개념 정리

### 10.1 DTO (Data Transfer Object)
- **역할**: 계층 간 데이터 전송
- **이유**: Entity를 직접 노출하면 보안 위험
```java
public class UserDTO {
    private String username;
    private String email;
    // password는 포함하지 않음!
}
```

### 10.2 Lombok
- **역할**: Getter/Setter, Constructor 자동 생성
```java
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class User {
    private Long id;
    private String username;
}
```

### 10.3 DevTools
- **역할**: 코드 수정 시 자동 재시작
```gradle
implementation 'org.springframework.boot:spring-boot-devtools'
```

### 10.4 REST API 기본
```
GET    /api/users       - 목록 조회
GET    /api/users/{id}  - 단건 조회
POST   /api/users       - 생성
PUT    /api/users/{id}  - 수정
DELETE /api/users/{id}  - 삭제
```

---

## 🎓 Chapter 11: 신입 개발자가 꼭 알아야 할 것들

### 11.1 프로젝트 구조는 '컨벤션'
- 회사마다 조금씩 다를 수 있음
- 하지만 MVC 패턴은 대부분 동일

### 11.2 에러 읽는 법
- **Stack Trace**: 아래에서 위로 읽기
- **Caused by**: 실제 원인
- 구글링: "[에러 메시지] spring boot"

### 11.3 로그 활용
```java
@Slf4j  // Lombok
public class UserService {
    public void createUser() {
        log.info("사용자 생성 시작");
        log.debug("디버그 정보");
        log.error("에러 발생", exception);
    }
}
```

### 11.4 테스트 코드 (중요!)
```java
@Test
public void 사용자_생성_테스트() {
    // given
    User user = new User("john", "password");
    
    // when
    User savedUser = userRepository.save(user);
    
    // then
    assertThat(savedUser.getId()).isNotNull();
}
```

### 11.5 Git 커밋 메시지
```
feat: 사용자 로그인 기능 추가
fix: 비밀번호 암호화 버그 수정
refactor: 코드 리팩토링
docs: README 업데이트
```

---

## ⚠️ Chapter 12: 실무에서 하지 말아야 할 것들

1. **비밀번호 평문 저장** → BCrypt 사용!
2. **application.properties에 민감정보** → 환경변수 사용
3. **모든 API를 public으로** → 권한 체크 필수
4. **예외 처리 안 함** → try-catch 또는 @ControllerAdvice
5. **SQL Injection 방어 안 함** → JPA 사용하면 기본 방어됨

---

## 📝 Chapter 13: 체크리스트 (프로젝트 시작 전)

- [ ] JDK 17 이상 설치
- [ ] IDE (Eclipse/IntelliJ) 설치
- [ ] MySQL 설치 및 Schema 생성
- [ ] build.gradle 의존성 확인
- [ ] application.properties 설정
- [ ] 포트 충돌 확인 (8080, 3306)
- [ ] Git 저장소 생성
- [ ] .gitignore 설정 (application.properties 제외)

---

이 정리가 네가 실무에서 Spring Boot 프로젝트를 시작할 때 든든한 가이드가 되었으면 좋겠어! 

**핵심 3줄 요약:**
1. Spring Boot = 백엔드 개발 프레임워크 (Java 기반)
2. MVC 패턴 + JPA로 데이터베이스 연동
3. application.properties에서 모든 환경 설정 관리

화이팅! 궁금한 점 있으면 언제든 물어봐! 🚀