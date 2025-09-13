import java.util.Scanner;

public class ConditionFlowDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("=== 조건문 실행 흐름 분석 ===");
        
        // 사용자로부터 점수 입력받기
        System.out.print("점수를 입력하세요 (0-100): ");
        int testValue = scanner.nextInt();
        
        System.out.println("입력된 값: " + testValue);
        System.out.println("조건 검사 시작...");
        
        // 논리 연산자로 boolean 값 생성
        boolean isExcellent = testValue > 90;    // 우수한 성적
        boolean isGood = testValue > 80;         // 좋은 성적
        boolean isAverage = testValue > 70;      // 보통 성적
        boolean isPassing = testValue >= 60;     // 합격선
        
        System.out.println("\n=== 논리 연산자로 생성된 boolean 값들 ===");
        System.out.println("우수한 성적 (>90): " + isExcellent);
        System.out.println("좋은 성적 (>80): " + isGood);
        System.out.println("보통 성적 (>70): " + isAverage);
        System.out.println("합격선 (>=60): " + isPassing);
        
        System.out.println("\n=== Boolean 값을 활용한 if문 실행 ===");
        
        // boolean 변수를 사용한 if문
        if (isExcellent) {
            System.out.println("등급: A - 우수한 성적입니다!");
        } else if (isGood) {
            System.out.println("등급: B - 좋은 성적입니다!");
        } else if (isAverage) {
            System.out.println("등급: C - 보통 성적입니다!");
        } else if (isPassing) {
            System.out.println("등급: D - 합격입니다!");
        } else {
            System.out.println("등급: F - 불합격입니다.");
        }
        
        // 복합 논리 연산자 활용
        System.out.println("\n=== 복합 논리 연산자 활용 ===");
        
        boolean isHighAchiever = isExcellent && testValue >= 95;  // AND 연산
        boolean needsImprovement = !isPassing || testValue < 50;  // NOT과 OR 연산
        
        System.out.println("최고 성취자 (95점 이상): " + isHighAchiever);
        System.out.println("개선이 필요함: " + needsImprovement);
        
        if (isHighAchiever) {
            System.out.println("축하합니다! 최고 성취자입니다!");
        }
        
        if (needsImprovement) {
            System.out.println("더 열심히 공부해야 합니다.");
        }
        
        // 추가 분석
        System.out.println("\n=== 상세 분석 ===");
        
        // 등급 범위별 boolean 변수
        boolean isAGrade = testValue >= 90 && testValue <= 100;
        boolean isBGrade = testValue >= 80 && testValue < 90;
        boolean isCGrade = testValue >= 70 && testValue < 80;
        
        System.out.println("A등급 범위 (90-100): " + isAGrade);
        System.out.println("B등급 범위 (80-89): " + isBGrade);
        System.out.println("C등급 범위 (70-79): " + isCGrade);
        
        scanner.close();
    }
}