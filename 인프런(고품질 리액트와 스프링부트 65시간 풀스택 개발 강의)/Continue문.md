인프런 강의의 Java Switch문과 중첩 조건문 스크립트를 바탕으로 Eclipse IDE 실습 중심의 가이드를 작성했습니다.
핵심 내용:
1. Switch문의 기본 구조

소괄호 안에 비교할 변수 (int, char, String 등)
case문으로 각각의 경우 처리
break문의 중요성 (없으면 fall-through 발생)

2. 중첩 조건문 (Switch + if)

Switch문 안에 if문을 중첩하여 복잡한 조건 처리
실제 날씨 시스템, 사용자 등급 시스템 등 실무 예제

3. Eclipse 실습 코드 구성

기본 Switch문부터 복합 조건문까지 단계별 진행
강의에서 언급한 withFact, p6spy 등의 실제 예제 반영
break문이 있는 경우와 없는 경우의 차이점 명확히 제시

4. 실무적 활용

메뉴 선택 시스템
사용자 레벨별 권한 처리
날씨 기반 조건 분기
Switch vs if문 성능 비교

강의에서 강조한 "break문의 중요성"과 "중첩 조건문의 흐름 파악"을 중점적으로 다뤘으며, Eclipse에서 직접 타이핑하며 각 케이스의 실행 흐름을 눈으로 확인할 수 있도록 상세한 출력문을 포함했습니다.

# Java Continue문 - Eclipse IDE 실습 가이드

## 1. Continue문의 기본 개념

### Continue문 소개
강의에서 설명한 핵심 개념:
- **우클릭하시고 U에다가 패키지 하시고요**
- **그 다음에 P1,U1 컨티뉴하고 이렇게 입력할게요**
- **이렇게 하시고 이걸 컨티뉴 키워드 할게요**

### Continue문의 역할
- **자 이번에는 continue. continue 키워드에 대해서 배워보도록 할게요**
- **java의 continue 키워드입니다**
- **보시면 제가 코드를 작성해서 예시를 보여드릴게요**

## 2. For문과 Continue의 조합

### 기본 For문 구조
- **for 반복문을 써볼게요**
- **for int i = 1부터 그 다음에는 10까지**
- **i++이라고 할게요**

### Continue의 동작 원리
- **이렇게 하시고요 그 다음에 if 의 값이 나머지가 0과 같다면 이제 continue**
- **라는 키워드를 써봐**

## 3. Eclipse IDE 실습 코드

### 기본 Continue문 예제

```java
package p1_variable;

public class ContinueDemo {
    public static void main(String[] args) {
        System.out.println("=== Continue문 기본 실습 ===");
        
        // 강의에서 설명한 기본 for문과 continue
        for (int i = 1; i <= 10; i++) {
            // 짝수일 때 continue 실행
            if (i % 2 == 0) {
                continue;  // 나머지 코드를 건너뛰고 다음 반복으로
            }
            
            System.out.println("홀수: " + i);
        }
        
        System.out.println("for문 실행 완료");
    }
}
```

### 강의 내용 기반 상세 예제

```java
package p1_variable;

public class ContinueDetailDemo {
    public static void main(String[] args) {
        System.out.println("=== Continue문 상세 분석 ===");
        
        // "이제 출수려면 아래 나머지가 2인 값이 0이라는 걸 뭐냐면 이제 짝수잖아 짝수잇데"
        // "아래 나머지가 2인 값이 0이면 짝수잖아 짝수라면 그리고 이거는 뭐예요?"
        
        System.out.println("1부터 10까지 숫자 중 홀수만 출력:");
        
        for (int i = 1; i <= 10; i++) {
            System.out.println("현재 i 값: " + i + " (반복 시작)");
            
            // "1부터 2부터 3,4,5,6,7,8,9,10까지 나오죠"
            // "10까지 전부 다 아해하니까 할을 시켜서 일시 중갑시킨거고 이 초개를 중에서 짝수라면"
            
            if (i % 2 == 0) {
                System.out.println("  -> " + i + "는 짝수이므로 continue 실행");
                continue;  // 짝수면 아래 코드 건너뛰기
            }
            
            // continue가 실행되면 이 부분은 건너뛰어짐
            System.out.println("  -> " + i + "는 홀수이므로 출력됩니다!");
            System.out.println("==================");
        }
        
        // "continue 하면요 이제 무슨 말일까요"
        // "continue 키워드가 있는데 이제 자바에서 무슨 의미냐면"
        System.out.println("반복문 완료!");
    }
}
```

### Continue의 흐름 제어 이해

```java
package p1_variable;

public class ContinueFlowDemo {
    public static void main(String[] args) {
        System.out.println("=== Continue 흐름 제어 분석 ===");
        
        // "바로 해당 if 조건문 안에 조건에 해당하는 코드를 생략하더는 뜻입니다"
        // "무슨말이냐면 짝수에 계산된 이 코드 있죠"
        
        System.out.println("조건별 실행 흐름:");
        
        for (int i = 1; i <= 5; i++) {
            System.out.println("\n--- 반복 " + i + "번째 시작 ---");
            
            // 조건 확인
            if (i == 3) {
                System.out.println("i가 3이므로 continue 실행!");
                continue;
            }
            
            // continue가 실행되지 않을 때만 실행되는 코드들
            System.out.println("첫 번째 출력: " + i);
            System.out.println("두 번째 출력: " + (i * 2));
            System.out.println("세 번째 출력: 반복 완료");
        }
        
        // "이것들 중에서 짝수를 모두 생략해라"
        System.out.println("\n전체 반복문 종료");
    }
}
```

## 4. Continue vs Break 비교

### Continue와 Break의 차이점

```java
package p1_variable;

public class ContinueVsBreakDemo {
    public static void main(String[] args) {
        System.out.println("=== Continue vs Break 비교 ===");
        
        System.out.println("1. Continue 사용 (특정 조건만 건너뛰기):");
        for (int i = 1; i <= 5; i++) {
            if (i == 3) {
                System.out.println("  i=" + i + ": continue로 건너뛰기");
                continue;
            }
            System.out.println("  i=" + i + ": 정상 실행");
        }
        System.out.println("Continue: 반복문 완료\n");
        
        System.out.println("2. Break 사용 (반복문 완전 종료):");
        for (int i = 1; i <= 5; i++) {
            if (i == 3) {
                System.out.println("  i=" + i + ": break로 반복문 종료");
                break;
            }
            System.out.println("  i=" + i + ": 정상 실행");
        }
        System.out.println("Break: 반복문 조기 종료");
        
        // "이렇데요. 짝착고 그럼다면 무슨말이냐면 이제 i 변수에서 짝수를 생략하는"
        // "1,3,5,7,9만 나늬지죠"
    }
}
```

## 5. 실무적 Continue 활용

### 데이터 필터링 예제

```java
package p1_variable;

public class ContinuePracticalDemo {
    public static void main(String[] args) {
        System.out.println("=== Continue 실무 활용 예제 ===");
        
        // "그리고 이제"
        // "이건 짝수가 아니고 어.."
        // "짝수가 아니고 홀수가 출력되겠네요"
        
        int[] scores = {85, 45, 92, 67, 38, 88, 73, 29, 95, 51};
        
        System.out.println("60점 이상인 점수만 출력:");
        for (int i = 0; i < scores.length; i++) {
            // 60점 미만이면 건너뛰기
            if (scores[i] < 60) {
                System.out.println("점수 " + scores[i] + ": 60점 미만으로 건너뛰기");
                continue;
            }
            
            // 60점 이상만 처리
            System.out.println("합격 점수: " + scores[i] + "점");
        }
        
        // "홀수 홀수입니다 홀수 홀수만 출력이 됨답"
        // "이렇게 할 수가 있는 거예요 홀수만 출력되지지고 해복겠습니다"
        
        System.out.println("\n=== 특정 조건 제외하고 처리 ===");
        
        String[] names = {"김철수", "", "이영희", "박민수", "", "최진우"};
        
        for (int i = 0; i < names.length; i++) {
            // 빈 문자열은 건너뛰기
            if (names[i].equals("")) {
                System.out.println("빈 이름 발견 - continue로 건너뛰기");
                continue;
            }
            
            System.out.println("처리할 이름: " + names[i]);
        }
    }
}
```

### 중첩 반복문에서의 Continue

```java
package p1_variable;

public class NestedContinueDemo {
    public static void main(String[] args) {
        System.out.println("=== 중첩 반복문에서 Continue 활용 ===");
        
        // "콘솔은 챗찰리게 쓰데요"
        // "아까 짝수가 쓴 것은 출력해볼게요"
        
        System.out.println("구구단에서 특정 조건 제외:");
        
        for (int i = 2; i <= 4; i++) {
            System.out.println("\n" + i + "단:");
            
            for (int j = 1; j <= 9; j++) {
                // 결과가 짝수인 경우 건너뛰기
                if ((i * j) % 2 == 0) {
                    continue;
                }
                
                System.out.println(i + " × " + j + " = " + (i * j));
            }
        }
        
        // "이렇게 해보고 그 다음에 실행시켜보면 이제 홀수만 1, 3, 5, 7, 9가 출력되는 걸 확인할"
        // "수가 있어요. 이렇게 해서 이렇게 표현할 수 있고 또 다른 방법이 있습니다"
        
        System.out.println("\n=== 조건부 데이터 처리 ===");
        
        for (int day = 1; day <= 7; day++) {
            // 주말(토요일=6, 일요일=7) 건너뛰기
            if (day == 6 || day == 7) {
                System.out.println("Day " + day + ": 주말이므로 업무 없음 (continue)");
                continue;
            }
            
            System.out.println("Day " + day + ": 평일 업무 수행");
        }
    }
}
```

## 6. Continue 키워드의 핵심 이해

### Continue의 정확한 동작 방식

```java
package p1_variable;

public class ContinueMechanismDemo {
    public static void main(String[] args) {
        System.out.println("=== Continue 동작 메커니즘 ===");
        
        // "이번에는 또 재밌게 해보고 싶어서 한 번 더 해볼 건데 바로 짝수만 출력해 거예요"
        // "그럼 어떻게 할까요?"
        // "바로 이렇게 이렇게 해가지고 이렇데도 가능하죠"
        
        System.out.println("Continue 실행 전후 코드 흐름:");
        
        for (int i = 1; i <= 5; i++) {
            System.out.println("  [시작] i = " + i);
            
            if (i == 3) {
                System.out.println("  [조건 만족] i가 3이므로 continue 실행");
                continue;  // 여기서 반복의 나머지 부분을 건너뛰고 다음 i로
            }
            
            System.out.println("  [continue 후 코드] 이 부분은 i=3일 때 실행되지 않음");
            System.out.println("  [처리 완료] i = " + i + " 처리 끝");
            System.out.println("  ----------------------");
        }
        
        // "이렇게 하면 어떻게 될까요?"
        // "00이 아니라는 거죠"
        
        System.out.println("\n=== Continue의 실제 효과 확인 ===");
        
        int processedCount = 0;
        int skippedCount = 0;
        
        for (int i = 1; i <= 10; i++) {
            if (i % 3 == 0) {  // 3의 배수는 건너뛰기
                skippedCount++;
                System.out.println("Skip: " + i + " (3의 배수)");
                continue;
            }
            
            processedCount++;
            System.out.println("Process: " + i);
        }
        
        System.out.println("\n처리된 항목: " + processedCount + "개");
        System.out.println("건너뛴 항목: " + skippedCount + "개");
        
        // "나머지 2가 0이 아니라는 건요 여러분 홀이 예기하는 겁니다"
        // "뽑수. 그럼 이제 뭐가 나을까요?"
        // "2,4,6,8,10만 나는 겁니다"
    }
}
```

## 7. Eclipse에서 실습하기

### 단계별 실습 가이드

1. **새 패키지 및 클래스 생성**
   - Package Explorer에서 우클릭
   - New → Package → `p1_variable`
   - 새 클래스: `ContinuePractice`

2. **기본 Continue문 연습**
```java
package p1_variable;

public class ContinuePractice {
    public static void main(String[] args) {
        // 1단계: 기본 continue 이해
        System.out.println("=== 기본 Continue 연습 ===");
        
        for (int i = 1; i <= 5; i++) {
            if (i == 3) {
                continue;  // i가 3일 때 건너뛰기
            }
            System.out.println("숫자: " + i);
        }
        
        // 2단계: 조건부 continue
        System.out.println("\n=== 짝수 건너뛰기 ===");
        
        for (int i = 1; i <= 10; i++) {
            if (i % 2 == 0) {
                continue;  // 짝수 건너뛰기
            }
            System.out.println("홀수: " + i);
        }
        
        // 3단계: 실용적 활용
        System.out.println("\n=== 유효한 데이터만 처리 ===");
        
        int[] data = {10, -5, 8, 0, 15, -3, 12};
        
        for (int value : data) {
            if (value <= 0) {
                System.out.println("음수 또는 0 건너뛰기: " + value);
                continue;
            }
            System.out.println("처리: " + value + " → " + (value * 2));
        }
    }
}
```

3. **실행 및 결과 분석**
   - Ctrl + F11로 실행
   - Console에서 continue가 어떤 값들을 건너뛰는지 확인
   - 조건을 변경하며 다른 패턴 테스트

## 핵심 정리

1. **Continue는 현재 반복의 나머지 부분을 건너뛰고 다음 반복으로 이동**
2. **Break와 달리 반복문을 완전히 종료하지 않고 특정 조건만 제외**
3. **데이터 필터링이나 조건부 처리에 유용**
4. **중첩 반복문에서는 가장 안쪽 반복문에만 영향**
5. **코드의 가독성을 높이고 불필요한 처리를 방지**

Continue문은 반복문에서 특정 조건을 만족하는 경우에만 처리를 건너뛰고 싶을 때 사용하는 강력한 제어 구조입니다. Eclipse에서 직접 다양한 조건을 테스트해보며 continue의 동작 방식을 체득하는 것이 중요합니다.