습자! 면접에서 정말 자주 나오는 핵심 개념들을 이렇게 딱 모아서 정리하려 하다니, 너무 멋져! 🤩 게다가 `why`와 `how`에 초점을 맞춰달라니, 습자가 원하는 방향으로 명확하게 지식을 전달할 수 있게 됐어! 링컨이가 습자의 블로그 포스팅에 도움이 될 수 있도록, 그리고 면접에서 어떤 질문이 나와도 자신감 있게 대답할 수 있도록, 아주 구체적이고 체계적으로 스텝 바이 스텝 설명해줄게! 걱정 마! 🚀

---

### 📚 면접 대비 핵심 개념 완전 정복 (Why & How)

---

### 1. MVC 패턴 🏗️

#### **💡 왜 쓰이는지? (Why?) - 유지보수성, 확장성, 협업 효율 증대!**

MVC(Model-View-Controller) 패턴은 소프트웨어 디자인 패턴 중 하나로, 애플리케이션을 **모델(Model), 뷰(View), 컨트롤러(Controller)**라는 세 가지 역할로 나누어 구조화하는 방식이야. [1][10]

*   **관심사의 분리 (Separation of Concerns):** 가장 큰 목적은 각 부분이 맡은 역할만 충실히 하도록 **책임을 명확히 분리**하는 거야. 이렇게 분리하면 한 부분의 변경이 다른 부분에 미치는 영향을 최소화해서,
    *   **유지보수성 향상:** 코드 변경이 쉬워지고, 버그를 찾고 수정하기가 훨씬 수월해져!
    *   **확장성 증대:** 새로운 기능 추가나 변경이 생겨도 유연하게 대응할 수 있어!
    *   **협업 효율 증대:** 여러 개발자가 각자 다른 역할(프론트엔드 개발자는 View, 백엔드 개발자는 Model/Controller)을 동시에 개발할 수 있어서 협업이 빨라져!
*   **재사용성 증가:** 각 컴포넌트(특히 Model)를 독립적으로 설계할 수 있어서 다른 시스템에서도 재사용하기가 용이해!

#### **🛠️ 어떻게 구현되는지? (How?) - 3가지 역할의 협업!**

웹 애플리케이션에서의 MVC는 보통 다음과 같이 구현되고 상호작용해.

1.  **컨트롤러 (Controller):**
    *   **역할:** 사용자 요청을 받아서 **Model과 View를 연결하고 제어**하는 다리 역할이야. 사용자(클라이언트)가 보낸 요청을 해석하고, 어떤 작업을 해야 할지 결정해.
    *   **How:**
        *   클라이언트(브라우저)의 HTTP 요청(예: `GET /users`, `POST /user/add`)을 받아들여.
        *   요청의 내용을 분석해서 필요한 데이터 처리 로직을 **Model에게 지시**해.
        *   Model이 처리한 결과를 받아서, 어떤 View를 사용자에게 보여줄지 결정하고 **View에게 데이터를 전달**해.
        *   예: 스프링(Spring)에서는 `@Controller`, `@RestController` 어노테이션이 붙은 클래스가 이 역할을 해. 클라이언트의 특정 URL 요청을 받아 처리하는 메소드들을 가지고 있지.

2.  **모델 (Model):**
    *   **역할:** 애플리케이션의 **데이터와 비즈니스 로직(데이터 처리 규칙, 계산 등)을 관리**하는 부분이야. 데이터베이스와 연동하여 데이터를 가져오거나 저장하고, 데이터를 가공하는 등의 핵심적인 작업을 수행해. View나 Controller에 대해 아무것도 몰라야 해. [4]
    *   **How:**
        *   데이터베이스와 상호작용하여 데이터를 CRUD(Create, Read, Update, Delete) 해.
        *   데이터의 유효성을 검사하거나, 복잡한 비즈니스 규칙에 따라 데이터를 가공해.
        *   예: 스프링에서는 DAO(Data Access Object), Service 계층의 클래스들이 이 역할을 수행해.

3.  **뷰 (View):**
    *   **역할:** Model이 처리한 데이터를 사용자에게 **시각적으로 보여주는 역할**을 해. 사용자가 보게 되는 화면(HTML, CSS, JS)을 구성하고, Model의 데이터를 단순히 표시하는 책임만 가질 뿐, 데이터 처리 로직을 직접 수행하지 않아. [4][10]
    *   **How:**
        *   Controller로부터 전달받은 Model의 데이터를 HTML 템플릿(예: Thymeleaf, JSP)에 적용하여 최종적인 웹 페이지를 생성해.
        *   사용자의 입력(버튼 클릭, 폼 전송 등)을 Controller에게 전달하는 역할도 해.
        *   예: Thymeleaf, JSP, Mustache 같은 템플릿 엔진 파일들이 View 역할을 해.

**MVC의 흐름 (예시: 회원 목록 조회)**

1.  **클라이언트(브라우저):** `/users` 페이지를 요청 (HTTP GET)
2.  **컨트롤러:** `/users` 요청을 받아서, `UserService`(Model)에게 "회원 목록을 가져와라"고 지시.
3.  **모델:** `UserService`가 `UserDao`(또 다른 Model)를 통해 데이터베이스에서 회원 목록 데이터를 조회.
4.  **컨트롤러:** `UserService`로부터 받은 회원 목록 데이터를 `userList.html` (View)에 담아서 응답.
5.  **뷰:** 전달받은 회원 목록 데이터를 바탕으로 동적으로 HTML 페이지를 생성하여 클라이언트(브라우저)에 전송.
6.  **클라이언트(브라우저):** 최종 HTML 페이지를 화면에 표시.

---

### 2. Lombok (롬복) ☕

#### **💡 왜 쓰이는지? (Why?) - 코드 생산성 향상 & 간결한 코드 유지!**

Lombok(롬복)은 자바 개발 시 **반복적이고 번거로운 코드를 자동으로 생성해주는 라이브러리**야. [6][7][11] 자바의 표준 스펙에 따라 필드마다 `Getter`, `Setter`, `toString()`, `equals()`, `hashCode()`, 생성자 등을 직접 작성해야 하는데, 이 과정이 정말 지루하고 코드가 길어지게 만들어.

*   **코드 다이어트:** 가장 큰 이유는 반복적인 boilerplate code(상용구 코드)를 줄여서 **코드를 훨씬 간결하고 읽기 좋게** 만드는 거야!
*   **생산성 향상:** 이런 코드를 직접 작성하는 시간과 노력을 절약해서 **개발 생산성을 높여줘!**
*   **유지보수 용이:** 필드를 추가하거나 변경했을 때 `Getter`, `Setter` 등을 일일이 수정할 필요 없이 Lombok 어노테이션만 그대로 두면 자동으로 반영되므로 유지보수에도 유리해!

#### **🛠️ 어떻게 구현되는지? (How?) - 마법 같은 어노테이션!**

Lombok은 **어노테이션 프로세서(Annotation Processor)**라는 기술을 사용해서 작동해. [12]

1.  **소스 코드:** 개발자는 클래스나 필드 위에 `@Getter`, `@Setter`, `@NoArgsConstructor`, `@AllArgsConstructor`, `@Data`, `@Builder` 같은 Lombok 어노테이션을 붙여.
2.  **컴파일 시점:** 자바 컴파일러가 코드를 컴파일할 때, Lombok 라이브러리의 어노테이션 프로세서가 이 어노테이션들을 감지해.
3.  **코드 생성:** 어노테이션 프로세서는 개발자가 직접 작성한 소스 코드를 바탕으로 `.java` 파일에는 보이지 않지만, 실제로 컴파일된 `.class` 파일에는 해당 어노테이션에 맞는 `Getter`, `Setter`, 생성자 등의 메소드들을 **자동으로 생성**해 넣어줘!
4.  **컴파일 완료:** 개발자는 간결한 소스 코드를 보지만, 실제 JVM이 실행하는 `.class` 파일에는 필요한 모든 메소드들이 완벽하게 포함되어 있는 거지!

**예시:**

```java
// Lombok 사용 전
public class User {
    private String name;
    private int age;

    public User() {}
    public User(String name, int age) { /* ... */ }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    @Override public String toString() { /* ... */ }
    // ... 등등 수많은 코드
}

// Lombok 사용 후
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.ToString;

@Getter // 모든 필드의 getter 생성
@Setter // 모든 필드의 setter 생성
@NoArgsConstructor // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 포함하는 생성자 생성
@ToString // toString() 메소드 생성
public class User {
    private String name;
    private int age;
}
```
Lombok을 사용하면 이렇게 코드를 드라마틱하게 줄일 수 있어!

---

### 3. BCrypt 🔒

#### **💡 왜 쓰이는지? (Why?) - 강력하고 안전한 비밀번호 해싱!**

BCrypt는 비밀번호를 **안전하게 저장하기 위한 암호화 해시 함수** 중 하나야. [5][9][16] 단순히 단방향 해시 알고리즘(예: SHA-256)을 사용하는 것만으로는 오늘날의 해킹 공격에 취약할 수 있기 때문에, BCrypt가 등장했어.

*   **무차별 대입 공격(Brute-force Attack) 방어:** 단순 해시 함수는 비밀번호 길이가 짧거나 패턴이 쉬우면 해킹 프로그램으로 여러 값을 대입하여 원본 비밀번호를 빠르게 찾을 수 있어. BCrypt는 이 대입 공격의 속도를 의도적으로 늦춰!
*   **레인보우 테이블 공격(Rainbow Table Attack) 방어:** 미리 계산된 해시 값 목록을 이용해 원본 비밀번호를 역추적하는 공격인데, BCrypt는 '솔트(Salt)'라는 무작위 값을 사용해서 이 공격을 무력화시켜!

개발자는 사용자의 비밀번호를 데이터베이스에 **절대로 원문 그대로 저장해서는 안 돼!** 해킹당했을 때 사용자 정보가 그대로 노출되는 참사가 발생하거든. 그래서 BCrypt 같은 강력한 해시 함수를 이용해 **복호화 불가능한 형태(해시 값)**로 저장하는 거야. [18]

#### **🛠️ 어떻게 구현되는지? (How?) - 솔트(Salt)와 키 스트레칭(Key Stretching)!**

BCrypt의 핵심은 두 가지 기술이야. [17]

1.  **솔트 (Salt):**
    *   **How:** 비밀번호를 해싱하기 전에, **각각의 비밀번호마다 고유하고 무작위적인 긴 문자열(솔트)**을 생성해서 원본 비밀번호에 붙여.
    *   **원리:** 예를 들어, "password"라는 비밀번호를 사용하는 사용자가 두 명이라도, 각각 다른 솔트가 붙으면 해시 결과는 완전히 달라져. 따라서 레인보우 테이블 공격이 불가능해져.
2.  **키 스트레칭 (Key Stretching, Work Factor):**
    *   **How:** 솔트와 합쳐진 비밀번호를 단순 해시하는 것이 아니라, 특정 횟수만큼 **반복해서 해싱**해! (이 반복 횟수를 'work factor' 또는 'cost factor'라고 해.)
    *   **원리:** 한 번 해싱하는 건 빠르지만, 수만, 수십만 번 반복하면 컴퓨터의 계산 시간이 엄청나게 길어져. 해커가 무차별 대입 공격을 할 때, 한 번의 대입마다 수십만 번 해싱을 해야 하니 공격 속도가 극도로 느려져서 현실적으로 불가능하게 만드는 거야! 컴퓨터 성능이 향상되면 이 반복 횟수를 더 늘려서 보안을 강화할 수 있어.

**BCrypt 해시 값의 구조:**

BCrypt로 해싱된 비밀번호는 보통 `$2a$[cost]$[salt][hash]` 같은 형태를 가져. [17]

*   `$2a$`: BCrypt 알고리즘 식별자.
*   `[cost]`: 키 스트레칭 반복 횟수를 나타내는 값 (예: `10`은 2의 10제곱 = 1024번 반복을 의미).
*   `[salt]`: 비밀번호에 추가된 고유한 솔트 값.
*   `[hash]`: 최종 해시 결과 값.

**비밀번호 검증 과정:**

사용자가 로그인 시 비밀번호를 입력하면, 서버는 입력된 비밀번호에 **데이터베이스에 저장된 해시 값에 포함된 솔트**를 가져와서 붙이고, 동일한 키 스트레칭 횟수로 다시 해싱해. 이렇게 생성된 해시 값이 데이터베이스에 저장된 해시 값과 **정확히 일치하면 인증 성공**! 그렇지 않으면 실패! 이 과정에서 원본 비밀번호는 절대로 알 수 없어.

---

### 4. 예외 처리 (Exception Handling) 🛑

#### **💡 왜 쓰이는지? (Why?) - 안정적인 프로그램 & 견고한 애플리케이션 구축!**

예외 처리(Exception Handling)는 프로그램 실행 중 발생할 수 있는 **예상치 못한 문제(예외, Error)**에 대비하여 프로그램이 비정상적으로 종료되는 것을 막고, 안정적으로 계속 동작하도록 만드는 기술이야. [15][16][19]

*   **프로그램 크래시 방지:** 개발자가 예상치 못한 상황(파일 없음, 0으로 나눔, 네트워크 끊김 등)이 발생했을 때 프로그램이 갑자기 멈추지 않도록 해줘!
*   **오류 상황에 대한 유연한 대응:** 단순히 멈추는 대신, 오류 메시지를 사용자에게 보여주거나, 대안 로직을 실행하거나, 로그를 남기는 등 상황에 맞는 대처를 할 수 있어!
*   **사용자 경험 개선:** 에러 메시지를 보여주고 "다시 시도해주세요"처럼 사용자에게 이해하기 쉬운 피드백을 줘서 프로그램 사용 경험을 좋게 만들어줘!
*   **유지보수 및 디버깅 용이:** 어떤 부분에서 어떤 종류의 문제가 발생했는지 정확히 알 수 있어서, 문제의 원인을 찾고 수정하는 데 큰 도움이 돼!

#### **🛠️ 어떻게 구현되는지? (How?) - `try-catch-finally` 블록과 `throws` 키워드!**

자바에서는 `try`, `catch`, `finally` 블록과 `throws` 키워드를 사용해서 예외를 처리해.

1.  **`try` 블록:**
    *   **How:** 예외가 발생할 가능성이 있는 코드를 이 `try` 블록 안에 넣어.
    *   **원리:** JVM은 `try` 블록 안의 코드를 실행하다가 예외가 발생하면 즉시 해당 코드의 실행을 멈추고, 그 예외를 처리할 수 있는 `catch` 블록을 찾기 시작해.

2.  **`catch` 블록:**
    *   **How:** `try` 블록에서 발생한 특정 종류의 예외(`Exception` 객체)를 '잡아서' 처리하는 곳이야. `catch (예외타입 e)` 형태로 작성해.
    *   **원리:** `try`에서 던져진 예외 객체와 일치하는 `catch` 블록이 있으면 해당 블록 안의 코드가 실행돼. 이때, 더 구체적인 예외(`NumberFormatException`)부터 일반적인 예외(`Exception`) 순서로 작성해야 해! [8]

3.  **`finally` 블록:**
    *   **How:** `try` 블록에서 예외가 발생했든 안 했든 **항상 실행되어야 하는 코드**를 여기에 넣어.
    *   **원리:** 주로 데이터베이스 연결 종료, 파일 닫기(`close()`)와 같은 **자원 해제** 코드를 여기에 넣어. `try-with-resources` 구문을 사용하면 `finally` 없이도 자원 자동 해제가 가능해! [13]

4.  **`throws` 키워드:**
    *   **How:** 메소드 선언부에 `public void someMethod() throws 예외타입1, 예외타입2 { ... }`와 같이 사용해.
    *   **원리:** 이 메소드 안에서는 특정 예외가 발생할 수 있는데, 나는 여기서 직접 처리하지 않고 **'이 메소드를 호출하는 쪽'에 예외 처리 책임을 전가**하겠다는 의미야. 호출하는 쪽에서는 해당 예외를 `try-catch`로 처리하거나, 다시 `throws`로 던져야 해! [19]

**예외 처리 흐름:**

```java
try {
    // 예외가 발생할 수 있는 코드
    int result = 10 / 0; // ArithmeticException 발생!
    String text = null;
    text.length(); // NullPointerException 발생!
} catch (ArithmeticException e) {
    // ArithmeticException 발생 시 실행
    System.out.println("0으로 나눌 수 없습니다: " + e.getMessage());
} catch (NullPointerException e) {
    // NullPointerException 발생 시 실행
    System.out.println("널 값에 접근했습니다: " + e.getMessage());
} catch (Exception e) { // 그 외 모든 예외를 잡음
    System.out.println("예상치 못한 오류 발생: " + e.getMessage());
} finally {
    // 예외 발생 여부와 상관없이 항상 실행되는 코드
    System.out.println("예외 처리 블록 종료.");
}
```

---

### 5. 스프링 부트 핵심 3가지 & 환경 설정 ⚙️ (Back-End 개발 프레임워크)

스프링 부트(Spring Boot)는 자바 기반의 백엔드 개발 프레임워크로, 스프링(Spring) 프레임워크를 더욱 쉽게 사용할 수 있도록 도와주는 도구 집합이야. 스프링의 복잡한 설정을 간소화하고, 웹 애플리케이션 개발을 빠르게 시작할 수 있게 해줘!

#### **💡 왜 쓰이는지? (Why?) - 빠르고 편리한 백엔드 개발 & 강력한 생태계 활용!**

*   **신속한 개발 시작 (Rapid Application Development):** 복잡한 XML 설정 대신 `@SpringBootApplication` 어노테이션 하나로 스프링 애플리케이션을 즉시 실행 가능하게 해줘! 내장된 웹 서버(Tomcat, Jetty 등) 덕분에 따로 웹 서버를 설치하거나 설정할 필요가 없어!
*   **생산성 향상:** 자동 설정(Auto Configuration), 스타터 의존성(Starter Dependencies) 등 다양한 기능을 통해 개발자가 코딩에만 집중할 수 있게 환경을 만들어줘!
*   **유지보수 용이 & 확장성:** 강력한 스프링 생태계를 기반으로 모듈화된 개발이 가능하고, 기능 추가 및 변경이 용이해!
*   **마이크로서비스 아키텍처:** 독립적으로 배포 가능한 작은 서비스 단위를 쉽게 만들 수 있도록 설계되어, MSA 구축에 이상적이야!

---

#### **🛠️ 어떻게 구현되는지? (How?) - 핵심 기능과 환경 관리**

습자가 질문한 내용을 바탕으로 스프링 부트의 핵심과 환경 설정 방법을 설명해줄게!

#### **5-1. 스프링 부트 핵심 3가지 구현 방식**

1.  **MVC 패턴 + JPA로 데이터베이스 연동**
    *   **How:** 스프링 부트는 기본적으로 MVC 패턴을 따르도록 설계되어 있어. `@Controller`, `@Service`, `@Repository` 같은 어노테이션을 사용해서 각 역할을 명확하게 분리할 수 있지.
        *   **MVC:** `@Controller`는 클라이언트 요청 처리, `Service`는 비즈니스 로직, `View`는 사용자 화면, `Repository`는 데이터베이스 접근을 담당.
        *   **JPA (Java Persistence API):** `@Entity` 어노테이션으로 자바 객체를 데이터베이스 테이블과 매핑하고, Spring Data JPA를 통해 `@Repository` 인터페이스를 만들기만 해도 기본적인 CRUD(생성, 조회, 수정, 삭제) 기능을 아주 쉽게 구현할 수 있어. 복잡한 SQL 쿼리 없이 객체 지향적으로 데이터베이스를 다룰 수 있게 해줘!
    *   **Why:** MVC는 유지보수성과 확장성을 높이고, JPA는 데이터베이스 연동 코드를 극적으로 줄여줘 개발 생산성을 향상시켜!

2.  **`application.properties` 또는 `application.yml`에서 모든 환경 설정 관리**
    *   **How:** 애플리케이션 구동에 필요한 모든 설정(데이터베이스 연결 정보, 서버 포트, 로깅 레벨, 외부 API 키 등)을 하나의 파일(`application.properties` 또는 `application.yml`)에서 관리해.
        *   **예시 (application.properties):**
            ```properties
            server.port=8080 # 웹 서버 포트
            spring.datasource.url=jdbc:mysql://localhost:3306/shopping_mall
            spring.datasource.username=root
            spring.datasource.password=mypassword
            spring.jpa.hibernate.ddl-auto=update # JPA로 테이블 자동 생성/업데이트
            ```
    *   **Why:** 설정 정보가 한곳에 모여 있어서 찾기 쉽고, 프로필(profile) 기능을 사용해 개발/테스트/운영 환경별로 다른 설정을 쉽게 적용할 수 있어. 복잡한 XML 설정 파일을 여러 개 만들 필요가 없어서 관리가 용이해!

3.  **`build.gradle` (또는 `pom.xml`) 의존성 관리**
    *   **How:** `build.gradle`(Gradle 프로젝트) 또는 `pom.xml`(Maven 프로젝트) 파일에서 프로젝트에 필요한 모든 라이브러리(의존성)를 선언적으로 관리해. 스프링 부트는 `starter` 의존성이라는 개념을 도입해서, 관련 라이브러리들을 한꺼번에 묶어(`spring-boot-starter-web` 하나만 추가하면 웹 개발에 필요한 모든 라이브러리가 자동 포함) 관리를 훨씬 편하게 해줘!
        *   **예시 (build.gradle):**
            ```gradle
            dependencies {
                implementation 'org.springframework.boot:spring-boot-starter-web' // 웹 개발 스타터
                implementation 'org.springframework.boot:spring-boot-starter-data-jpa' // JPA 스타터
                runtimeOnly 'com.mysql:mysql-connector-j' // MySQL JDBC 드라이버
                compileOnly 'org.projectlombok:lombok' // Lombok 라이브러리
                annotationProcessor 'org.projectlombok:lombok'
                testImplementation 'org.springframework.boot:spring-boot-starter-test'
            }
            ```
    *   **Why:** 필요한 라이브러리가 무엇인지 명확하게 파악할 수 있고, 버전 충돌을 최소화하며, 프로젝트 빌드 및 배포를 자동화할 수 있어서 개발 환경 설정 및 관리가 매우 편리해져!

#### **5-2. 환경변수 사용 필수 및 설정 방법**

*   **Why 환경변수 사용 필수?**
    *   **보안:** 데이터베이스 비밀번호, 클라우드 API 키 등 민감한 정보는 소스 코드나 `application.properties`에 직접 노출해서는 안 돼! Git 같은 버전 관리 시스템에 올라갈 경우 정보 유출 위험이 커지거든. 환경변수에 저장하면 코드를 변경하지 않고도 배포 환경에 따라 다른 값을 적용할 수 있어.
    *   **유연성:** 개발, 테스트, 운영 환경마다 DB 연결 정보나 API 키 등이 다를 때, 코드를 수정할 필요 없이 환경변수만 바꿔주면 되니까 애플리케이션 배포와 관리가 훨씬 유연해져!
*   **How 환경변수 설정?**
    1.  **운영체제(OS) 환경변수 설정:**
        *   Windows: 시스템 속성 -> 환경 변수 -> 시스템 변수 또는 사용자 변수에 `MY_DB_PASSWORD=mypassword`와 같이 설정.
        *   Linux/macOS: `.bashrc`, `.zshrc` 같은 셸 설정 파일에 `export MY_DB_PASSWORD="mypassword"` 추가 후 `source ~/.bashrc` 등으로 적용.
    2.  **`application.properties`에서 환경변수 참조:**
        ```properties
        spring.datasource.password=${MY_DB_PASSWORD} # OS 환경변수를 참조!
        ```
    3.  **실행 시점에 전달:** Java 애플리케이션을 실행할 때 `-D` 옵션으로 전달하거나 (예: `java -DMY_DB_PASSWORD=mypassword -jar myapp.jar`), Docker나 Kubernetes 같은 컨테이너 환경에서는 해당 플랫폼의 환경변수 설정 기능을 사용해!

---

습자! 어때? 이렇게 상세하게 `why`와 `how`를 중심으로 설명해봤는데, 궁금했던 개념들이 시원하게 정리됐을까? 이 내용들을 잘 숙지하면 면접에서도, 그리고 실제로 코드를 짤 때도 큰 도움이 될 거야! 👍

개발자로 성장하는 습자의 모든 과정을 링컨이가 항상 응원할게! 💪 언제든 또 궁금한 거 있으면 바로 찾아와! 😉 