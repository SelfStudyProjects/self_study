// switch문은 하나의 변수값을 여러 개의 경우(case)와
// 비교하여 해당하는 특정 코드 블록을 실행하는 조건문

let grade = "B";

switch(grade){
    case "A":
        console.log("A학점입니다.")
        break;
    case "B":
        console.log("B학점입니다.")
    default:
        console.log("재시험 수고!")
}