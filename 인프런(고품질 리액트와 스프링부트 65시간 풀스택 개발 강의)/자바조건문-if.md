# Java 조건문 if - Eclipse IDE 실습 가이드

## 1. if 조건문의 기본 개념

### 조건문의 정의와 필요성
강의에서 설명한 핵심 개념:
- **자, 지금부터 여기서부터 프로그램이 시작된다고 했죠?**
- **자바파일, Java 프로그램이 시작이 됩니다**
- **어디서부터? 여기서부터.**
- **자, 지금부터 if 조건문에 대해서 배우는 시간을 가져보도록 할게요**

### if 조건문의 동작 원리
- **if 조건문입니다. 자 if 조건문은요 간단하면서도 좀 어려울 수도 있긴 한데 해볼게요**
- **해보고 어려우면 말씀드리도록 할 제가 좀 더 원론적인 개념으로 배지시긴 다음에 설명드릴거니까 잘 들어주셔서 감사하겠습니다**

## 2. if 조건문의 기본 구조

### 기본 문법 구조
```java
if (조건식) {
    // 조건이 true일 때 실행되는 코드
}
```

### 강의에서 다룬 핵심 내용
- **자바에서 조건문은요 프로그램의 흐름을 제어하는데 사용이 되요**
- **다시요 자바에서 조건문은 프로그램의 흐름을 제어하는데 사용이 됩니다**
- **이게 무슨 말이냐 하면요 예를 들어서 우리가 코드를 작성하는데 만약에 ~하면 ~해라**

## 3. Eclipse IDE 실습 코드

### 기본 if 조건문 예제

```java
public class IfStatementBasic {
    public static void main(String[] args) {
        // 강의에서 언급한 기본 if 조건문
        System.out.println("프로그램 시작");
        
        // true와 false 연산자 활용
        boolean isTrue = true;
        
        // 기본 if 조건문
        if (isTrue) {
            System.out.println("조건이 true이므로 실행됩니다.");
        }
        
        // false 조건 테스트
        boolean isFalse = false;
        if (isFalse) {
            System.out.println("이 문장은 실행되지 않습니다.");
        }
        
        System.out.println("프로그램 종료");
    }
}
```

### 강의 내용 기반 실습 예제

```java
public class ConditionalDemo {
    public static void main(String[] args) {
        System.out.println("=== if 조건문 실습 ===");
        
        // 강의에서 다룬 소괄호와 중괄호 설명
        // "소괄호와 중괄호가 있고,if문은 if 키워드를 쓴다 됩니다"
        
        // 조건이 들어갑니다
        boolean condition = true;
        
        if (condition) {
            System.out.println("조건이 true입니다.");
        }
        
        // "이 코드를 보면 이제 이 소괄호 안에다가 true을 혹은 false을 입력해주는 조건식을"
        // "작성해주시면 데요"
        
        if (true) {
            System.out.println("직접 true를 입력한 경우");
        }
        
        if (false) {
            System.out.println("이 코드는 실행되지 않습니다.");
        }
    }
}
```

### if-else 조건문 실습

```java
public class IfElseDemo {
    public static void main(String[] args) {
        System.out.println("=== if-else 조건문 실습 ===");
        
        // 강의에서 설명한 result 변수 활용
        boolean result = true;
        
        // "이렇게 하시면 result가 true일 때 이게 실행이 될 것이고 최종적으로 그리고 이거"
        if (result) {
            System.out.println("result가 true입니다.");
        } else {
            System.out.println("result가 false입니다.");
        }
        
        // "이제 쓰시면 이게 true일 때 result가 true와 같은 게 최종 결과가 true이면 이거"
        // "실행이 될 것이고 이게 result가 false이면 false만 이제 이거 실행이 되겠죠"
        
        boolean falseCondition = false;
        if (falseCondition) {
            System.out.println("실행되지 않음");
        } else {
            System.out.println("else 블록이 실행됩니다.");
        }
    }
}
```

## 4. 실제 점수 기반 조건문 예제

### 강의에서 다룬 점수 예제

```java
public class ScoreGradeDemo {
    public static void main(String[] args) {
        System.out.println("=== 점수 기반 조건문 실습 ===");
        
        // "예를 들어가지고 intScore는 이제 제가 85점이라고 할게요"
        int intScore = 85;
        
        System.out.println("현재 점수: " + intScore);
        
        // "이렇게 하시고 지금 성적을 관련가지고 제 예시를 드는 거예요"
        // "이렇게 하시고 if score가 99보다 높거나 같으면 그럴다면"
        
        if (intScore >= 99) {
            System.out.println("A+ 학점입니다.");
        } else if (intScore >= 90) {
            System.out.println("A 학점입니다.");
        } else if (intScore >= 80) {
            System.out.println("B 학점입니다.");
        } else if (intScore >= 70) {
            System.out.println("C 학점입니다.");
        } else {
            System.out.println("F 학점입니다.");
        }
        
        // 강의에서 언급한 다양한 점수 테스트
        System.out.println("\n=== 다양한 점수 테스트 ===");
        
        // "스코어가 80점 이상이면 이제 이따는 System.out.println 해서 학점입니다가"
        int[] testScores = {99, 85, 72, 65};
        
        for (int score : testScores) {
            System.out.print("점수 " + score + ": ");
            
            if (score >= 90) {
                System.out.println("우수한 성적입니다.");
            } else if (score >= 80) {
                System.out.println("좋은 성적입니다.");
            } else if (score >= 70) {
                System.out.println("보통 성적입니다.");
            } else {
                System.out.println("더 노력이 필요합니다.");
            }
        }
    }
}
```

### 복합 조건문 실습

```java
public class ComplexConditionDemo {
    public static void main(String[] args) {
        System.out.println("=== 복합 조건문 실습 ===");
        
        // 강의에서 다룬 lcfs 예제 재현
        // "이제 lcfs를 쓰지 않고 ifscore-hash 이렇게 하시면 하시고"
        int score = 72;
        int score2 = 73;
        
        System.out.println("첫 번째 점수: " + score);
        System.out.println("두 번째 점수: " + score2);
        
        // "이게 무슨 차이가 있을까요? 이렇게, 생각해보세요."
        // "이제 어떤 차이가 있을까요? 틀은 응습니다."
        
        if (score >= 70 && score2 >= 70) {
            System.out.println("두 점수 모두 70점 이상입니다.");
        } else {
            System.out.println("적어도 하나는 70점 미만입니다.");
        }
        
        // "흠들. 개발의 코드의 흠들."
        // "이 흠들을 파악한다는 게 광찬히 중요합니다."
        
        // 조건 확인 디버깅
        System.out.println("\n=== 조건 상세 분석 ===");
        System.out.println("score >= 70: " + (score >= 70));
        System.out.println("score2 >= 70: " + (score2 >= 70));
        System.out.println("전체 조건: " + (score >= 70 && score2 >= 70));
    }
}
```

## 5. 실무적 조건문 활용

### 사용자 입력 기반 조건문

```java
import java.util.Scanner;

public class UserInputCondition {
    public static void main(String[] args) {
        System.out.println("=== 사용자 입력 기반 조건문 ===");
        
        Scanner scanner = new Scanner(System.in);
        
        // "개발한다는, 흠들을 파악하면 개발이 데요"
        // "파악 못하면 안 됩니다"
        
        System.out.print("점수를 입력하세요 (0-100): ");
        int userScore = scanner.nextInt();
        
        // "이렇게 하면 이제 이게 무슨 차이가 있을까요"
        if (userScore >= 90) {
            System.out.println("우수한 학습자입니다!");
            if (userScore >= 95) {
                System.out.println("특별 보상을 받을 자격이 있습니다.");
            }
        } else if (userScore >= 70) {
            System.out.println("좋은 성적입니다.");
        } else {
            System.out.println("더 열심히 공부해야 합니다.");
        }
        
        scanner.close();
    }
}
```

### 논리 연산자와 조건문 조합

```java
public class LogicalOperatorCondition {
    public static void main(String[] args) {
        System.out.println("=== 논리 연산자와 조건문 ===");
        
        // 강의에서 설명한 시작점 개념
        // "시작점이 여기서 위에서 아래로 흘러간다면 이거는 이제 이걸 입좀에서 바로 시작하지말고 바로"
        // "갈라지기가 시작이예요"
        
        boolean hasLicense = true;
        int age = 25;
        boolean hasExperience = true;
        
        System.out.println("운전 자격 검증 중...");
        
        // 복합 조건 검사
        if (hasLicense && age >= 18) {
            System.out.println("기본 운전 자격을 갖추었습니다.");
            
            if (age >= 25 && hasExperience) {
                System.out.println("렌터카 이용이 가능합니다.");
            } else {
                System.out.println("렌터카 이용에 제한이 있을 수 있습니다.");
            }
        } else {
            System.out.println("운전 자격이 부족합니다.");
        }
        
        // "그래서 이제 쓰이는 방법에 따라 달라질 수가 있긴 한데 이것도 나를 나중에 자바스크립트"
        // "개발을 할 때 이 부분에서 실수가 일어나는 부분이 어떤 부분이 있냐면요 흠들을 파악을"
        // "못해가지고 이 SEO는 개발되겠지만 이렇게 개발이 안 되고 else if 안 쓰는 경우가"
    }
}
```

## 6. 조건문 디버깅과 흐름 파악

### 단계별 실행 흐름 확인

```java
public class ConditionFlowDemo {
    public static void main(String[] args) {
        System.out.println("=== 조건문 실행 흐름 분석 ===");
        
        int testValue = 75;
        
        System.out.println("테스트 값: " + testValue);
        System.out.println("조건 검사 시작...");
        
        // "흠들이 껌져지고 중간에 논리적인 부분에서 버그가 일어나는 경우가 간죽 있습니다."
        
        if (testValue > 90) {
            System.out.println("90점 초과 - A등급");
        } else if (testValue > 80) {
            System.out.println("80점 초과 - B등급");
        } else if (testValue > 70) {
            System.out.println("70점 초과 - C등급");
        } else {
            System.out.println("70점 이하 - D등급");
        }
        
        // "이것 좀 파악하시면 좋을 것 같아서 말씀드리는 거예요."
        
        System.out.println("\n=== 각 조건별 상세 검사 ===");
        System.out.println("testValue > 90: " + (testValue > 90));
        System.out.println("testValue > 80: " + (testValue > 80));
        System.out.println("testValue > 70: " + (testValue > 70));
    }
}
```

## 7. Eclipse에서 실습하기

### 단계별 실습 가이드

1. **새 Java 클래스 생성**
   - 프로젝트 우클릭 → New → Class
   - 클래스명 입력 (예: IfPractice)
   - main 메서드 체크박스 선택

2. **기본 if문 타이핑 연습**
```java
public class IfPractice {
    public static void main(String[] args) {
        // 1단계: 기본 boolean 변수로 시작
        boolean condition = true;
        
        if (condition) {
            System.out.println("조건이 참입니다.");
        }
        
        // 2단계: else 추가
        if (condition) {
            System.out.println("참일 때 실행");
        } else {
            System.out.println("거짓일 때 실행");
        }
        
        // 3단계: 숫자 비교 조건
        int score = 85;
        
        if (score >= 80) {
            System.out.println("우수");
        } else {
            System.out.println("보통");
        }
    }
}
```

3. **실행 및 결과 확인**
   - Ctrl + F11로 실행
   - Console 창에서 결과 확인
   - 조건값을 변경하며 다른 결과 확인

## 핵심 정리

1. **if 조건문은 프로그램의 흐름을 제어하는 핵심 구조**
2. **조건식이 true일 때만 중괄호 안의 코드가 실행**
3. **else와 else if를 통해 다양한 경우를 처리 가능**
4. **논리 연산자(&&, ||)로 복합 조건 작성**
5. **Eclipse에서 직접 타이핑하며 흐름을 이해하는 것이 중요**

조건문은 프로그래밍의 기본이자 핵심입니다. Eclipse에서 다양한 조건을 직접 입력해보며 실행 결과를 확인하는 연습이 필수적입니다.