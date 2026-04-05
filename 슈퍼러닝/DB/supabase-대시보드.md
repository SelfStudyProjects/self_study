# 실시간 대시보드 & Supabase 연동 — 역공학 총정리 문서

> 작성 기준: `classday-office` 실제 코드 기반  
> 대상 독자: 중학생도 이해할 수 있도록 작성

---

## 0. 왜 만들었어? — 탄생 배경

클래스데이의 "오늘의 수업" 대시보드가 있어요.  
선생님이 출석을 기록하면, 대시보드에 출석 현황이 실시간으로 반영되는 기능이에요.

**기존 문제:** 

```
선생님 A가 출석 기록
  → 대시보드는 그대로 (변화 없음)
  → 다른 선생님이 수동으로 새로고침을 눌러야만 반영됨
```

**우리가 만든 것:**

```
선생님 A가 출석 기록
  → 대시보드가 자동으로 갱신됨
  → 새로고침 필요 없음!
```

이걸 구현하기 위해 **Supabase Realtime** 이라는 기술을 중간 다리로 사용해요.

---

## 1. 등장인물 소개 — 4명이 협력해요

```
① 선생님          → 출석 기록 버튼 클릭
② NestJS 서버     → MySQL에 저장 + Supabase에 신호 발송
③ Supabase        → "변경됐어!" 이벤트를 대시보드에 중계
④ React 대시보드  → 이벤트 받아서 자동 갱신
```

> 비유: 편의점 알바생(선생님)이 계산을 하면, POS 기기(NestJS)가
> 본사 서버(Supabase)에 신호를 보내고, 본사는 매장 관리 앱(대시보드)에
> "재고 변경됐어요!" 알림을 보내는 것.

---

## 2. 파일 지도 — 어떤 파일이 뭘 해?

### 백엔드 (`apps/api/src/`)

| 파일 | 역할 |
|---|---|
| `supabase/supabase.service.ts` | Supabase `attendance_signals` 테이블에 UPSERT |
| `supabase/supabase.module.ts` | SupabaseService를 NestJS에 등록 |
| `course/attendance/attendance.service.ts` | 출석 기록 후 Supabase에 신호 보냄 |
| `course/course.module.ts` | CourseModule에 SupabaseModule 연결 |
| `todayclass/todayclass.controller.ts` | `GET /spaces/:spaceId/todayclass` 엔드포인트 |
| `todayclass/todayclass.service.ts` | 컨트롤러 요청 처리, Repository 호출 |
| `todayclass/repositories/todayclass.repository.ts` | MySQL에서 오늘 수업 데이터 조회 |
| `todayclass/dto/todayclass.dto.ts` | 요청/응답 데이터 모양 정의 |
| `app.module.ts` | 앱 전체 모듈 등록 |

### 프론트엔드 (`apps/web/src/`)

| 파일 | 역할 |
|---|---|
| `lib/supabase.ts` | Supabase 연결 객체 초기화 (앱 전체 싱글턴) |
| `features/todayclass/hooks/use-todayclass.ts` | Supabase 구독 + React Query로 데이터 관리 |
| `features/todayclass/api/todayclass.api.ts` | 백엔드 API 호출 함수 |
| `features/todayclass/types/index.ts` | 백엔드 DTO와 1:1 매칭 TypeScript 타입 |
| `pages/TodayClassPage.tsx` | 실제 화면 UI |

---

## 3. 전체 흐름 요약

```
출석 기록
  → attendance.service.ts       (MySQL 저장 + 신호 발송)
  → supabase.service.ts         (attendance_signals 테이블 UPSERT)
  → Supabase Realtime           (변경 이벤트 중계)
  → use-todayclass.ts           (이벤트 수신 → React Query invalidate)
  → todayclass.api.ts           (백엔드 API 재호출)
  → TodayClassPage.tsx          (화면 자동 갱신)
```

---

## 4. 코드 완전 해부 (주석 포함)

---

### 4-1. `apps/api/src/supabase/supabase.service.ts`

> Supabase와 통신하는 유일한 창구. 출석 변경 시 "신호"를 보내는 역할.

```typescript
// NestJS에서 "이 클래스는 DI 컨테이너가 관리해도 돼" 라고 등록하는 데코레이터
import { Injectable } from "@nestjs/common";

// .env 파일의 환경 변수를 안전하게 읽어오는 NestJS 표준 서비스
import { ConfigService } from "@nestjs/config";

// Supabase 연결을 만드는 팩토리 함수 + 연결 객체의 타입
import { createClient, SupabaseClient } from "@supabase/supabase-js";

// NestJS DI 컨테이너에 등록 — 다른 모듈에서 주입받아 쓸 수 있음
@Injectable()
export class SupabaseService {

  // private: 클래스 내부에서만 접근 가능
  // readonly: 생성자에서 딱 한 번만 할당, 이후 절대 변경 불가
  // SupabaseClient: Supabase가 제공하는 연결 객체의 TypeScript 타입
  private readonly supabase: SupabaseClient;

  // 클래스 인스턴스가 처음 만들어질 때 딱 한 번 실행되는 초기화 함수
  // NestJS가 ConfigService 인스턴스를 자동으로 만들어서 여기 주입해줌 (DI)
  constructor(private readonly config: ConfigService) {

    // createClient: Supabase 서버와의 연결 채널을 열어주는 함수
    this.supabase = createClient(
      // getOrThrow: 값이 없으면 에러를 던져서 서버 시작 자체를 막음
      // <string>: 반환값이 string 타입임을 TypeScript에 알려주는 제네릭
      this.config.getOrThrow<string>("SUPABASE_URL"),

      // service_role key: RLS를 무시하고 모든 테이블에 접근 가능한 백엔드 전용 비밀 키
      // → 절대 프론트엔드 코드에 넣으면 안 됨 (보안 뚫림)
      this.config.getOrThrow<string>("SUPABASE_SERVICE_ROLE_KEY"),
    );
  }

  // async: 함수 내부에서 await 사용 가능, 호출자에게 Promise를 반환함
  // spaceId: 어느 학원에서 출석이 변경됐는지 식별하는 숫자
  // Promise<void>: 비동기 작업 완료 시 아무 값도 반환하지 않음 (완료 신호만)
  async signalAttendanceUpdated(spaceId: number): Promise<void> {

    // try: 아래 코드를 실행해보고, 에러가 나면 catch 블록으로 이동
    try {
      // await: UPSERT가 완료될 때까지 이 함수만 대기 (Node.js 전체는 안 멈춤)
      await this.supabase
        // attendance_signals 테이블을 대상으로 지정
        .from("attendance_signals")
        // UPSERT = UPDATE + INSERT 합성어
        // space_id가 이미 있으면 → pinged_at만 UPDATE
        // space_id가 없으면    → 새 행을 INSERT
        // pinged_at이 바뀌어야 Supabase Realtime이 "변경됐다!" 이벤트를 발생시킴
        // new Date().toISOString(): 현재 시각을 "2026-03-29T10:30:00.000Z" 형태 문자열로 변환
        .upsert({ space_id: spaceId, pinged_at: new Date().toISOString() });

    } catch {
      // Supabase 신호 전송 실패가 출석 기록 자체를 실패시키면 안 됨
      // → 출석 기록은 MySQL에 이미 저장 완료된 상태 (핵심 기능은 보호)
      // → catch로 에러를 삼키고 로그만 남김 (부가 기능 실패는 조용히 처리)
      console.error("[SupabaseService] signalAttendanceUpdated failed", spaceId);
    }
  }
}
```

---

### 4-2. `apps/api/src/supabase/supabase.module.ts`

> SupabaseService를 NestJS 모듈 시스템에 등록하고, 다른 모듈에 공개하는 파일.

```typescript
// NestJS 모듈을 정의할 때 쓰는 데코레이터를 가져옴
import { Module } from "@nestjs/common";

// 이 모듈에서 제공할 서비스 클래스를 가져옴
import { SupabaseService } from "./supabase.service";

// @Module: 이 클래스가 NestJS 모듈임을 선언하는 데코레이터
@Module({
  // providers: 이 모듈 안에서 생성하고 관리할 클래스 목록
  // NestJS DI 컨테이너가 SupabaseService 인스턴스를 만들어서 보관함
  providers: [SupabaseService],

  // exports: 다른 모듈이 import했을 때 꺼내 쓸 수 있도록 공개하는 목록
  // 여기 없으면 CourseModule에서 SupabaseService를 주입받을 수 없음
  exports: [SupabaseService],
})
// 클래스 본문이 비어 있는 이유: 모든 설정은 @Module 데코레이터 안에 다 들어 있음
export class SupabaseModule {}
```

---

### 4-3. `apps/api/src/course/course.module.ts` (핵심 수정 부분)

> AttendanceService가 SupabaseService를 쓸 수 있도록 CourseModule에 SupabaseModule을 연결.

```typescript
import { Module } from '@nestjs/common';
import { DatabaseModule } from '../database/database.module';
import { SpaceModule } from '../space/space.module';

// SupabaseModule을 가져옴 — 이게 없으면 AttendanceService에서 SupabaseService를 쓸 수 없음
import { SupabaseModule } from '../supabase/supabase.module';

// ... 기타 import 생략

@Module({
  // imports 배열에 SupabaseModule 추가
  // → "CourseModule 안에서 SupabaseService를 써도 돼" 라는 허락
  // → 이게 없으면 NestJS가 "SupabaseService를 찾을 수 없어!" 에러를 던짐
  imports: [DatabaseModule, SpaceModule, SupabaseModule, /* ... */],

  controllers: [
    // AttendanceController 등 여러 컨트롤러들
  ],
  providers: [
    // AttendanceService가 여기 등록되어 있음
    // AttendanceModule은 별도로 없고, CourseModule 안에 직접 포함됨
  ],
  exports: [/* ... */],
})
export class CourseModule {}
```

---

### 4-4. `apps/api/src/course/attendance/attendance.service.ts` (핵심 수정 부분)

> 출석을 MySQL에 저장한 뒤, Supabase에 신호를 보내는 핵심 지점.

```typescript
// SupabaseService를 이 파일에서 쓸 수 있도록 import
import { SupabaseService } from "../../supabase/supabase.service";

// ... 기타 import 생략

@Injectable()
export class AttendanceService {
  constructor(
    private readonly coursesRepo: CoursesRepository,
    private readonly attendanceRepo: AttendanceRepository,
    private readonly presetsService: AttendanceSheetPresetsService,
    private readonly attendanceAutoSendService: AttendanceAutoSendService,

    // NestJS가 SupabaseService 인스턴스를 자동으로 만들어서 여기 주입해줌
    // CourseModule이 SupabaseModule을 import했기 때문에 가능함
    private readonly supabaseService: SupabaseService,
  ) {}

  // 출석 기록을 저장하는 핵심 함수
  async upsertAttendanceRecord(spaceId: number, courseId: number, body: UpsertAttendanceRecordBodyDto) {

    // ... 유효성 검사 로직 생략 ...

    // ① MySQL DB에 출석 기록 저장 (핵심 기능)
    const row = await this.attendanceRepo.upsertAttendanceRecord({ ... });

    // ② 자동 알림 문자 발송 (비동기, 결과를 기다리지 않음)
    // void: 반환값을 무시하겠다는 명시적 표현
    const allowAutoSend = body.sendAutoNotification !== false;
    if (allowAutoSend) {
      void this.attendanceAutoSendService.sendIfEnabled({ ... });
    }

    // ③ Supabase에 신호 전송 ← 실시간 대시보드 갱신의 시작점!
    // MySQL 저장이 성공한 다음에 실행됨 (순서 중요)
    // try/catch는 SupabaseService 내부에서 처리하므로 여기서는 await만 호출
    // → 실패해도 출석 기록 결과에 영향 없음
    await this.supabaseService.signalAttendanceUpdated(spaceId);

    // 저장된 출석 데이터를 응답으로 반환
    return {
      attendanceRecordId: row.attendance_record_id,
      courseSessionId: row.course_session_id,
      enrollmentId: row.enrollment_id,
      status: row.status,
      // ... 나머지 필드
    };
  }
}
```

---

### 4-5. `apps/api/src/todayclass/todayclass.controller.ts`

> 프론트가 데이터를 요청할 때 받아주는 HTTP 입구.

```typescript
// NestJS HTTP 관련 데코레이터들
import { Controller, Get, Param, ParseIntPipe, Query, UseGuards } from "@nestjs/common";

// 이 학원의 멤버만 접근할 수 있도록 막는 보안 가드
import { SpaceAccessGuard } from "../space/guards/space-access.guard";

import { TodayClassService } from "./todayclass.service";
import { GetTodayClassQueryDto } from "./dto/todayclass.dto";

// @Controller: 이 클래스가 HTTP 요청을 받는 컨트롤러임을 선언
// "spaces/:spaceId/todayclass" → 실제 URL: /spaces/123/todayclass
@Controller("spaces/:spaceId/todayclass")

// @UseGuards: 이 컨트롤러의 모든 요청에 SpaceAccessGuard를 적용
// → 해당 학원 멤버가 아니면 접근 차단
@UseGuards(SpaceAccessGuard)
export class TodayClassController {

  // TodayClassService를 NestJS DI로 주입받음
  constructor(
    private readonly todayClassService: TodayClassService,
  ) {}

  // @Get(): HTTP GET 요청을 처리하는 메서드
  @Get()
  async getTodayClass(
    // @Param: URL 경로의 :spaceId 값을 추출
    // ParseIntPipe: 문자열 "123"을 숫자 123으로 자동 변환
    @Param("spaceId", ParseIntPipe) spaceId: number,

    // @Query: ?date=2026-03-29 같은 쿼리 파라미터를 DTO로 받음
    @Query() query: GetTodayClassQueryDto,
  ) {
    // date가 없으면 오늘 날짜를 기본값으로 사용
    // toISOString(): "2026-03-29T00:00:00.000Z" → slice(0, 10): "2026-03-29"
    const date =
      query.date ?? new Date().toISOString().slice(0, 10);

    // 실제 비즈니스 로직은 Service에 위임 (Controller는 라우팅만 담당)
    return this.todayClassService.getTodayClass(spaceId, date);
  }
}
```

---

### 4-6. `apps/api/src/todayclass/todayclass.service.ts`

> DB 데이터를 가져와서 API 응답 형태로 가공하는 곳.

```typescript
import { Injectable } from "@nestjs/common";
import type { ClassroomDto, ScheduleBlockDto, TodayClassResponseDto } from "./dto/todayclass.dto";
import { TodayClassRepository } from "./repositories/todayclass.repository";

@Injectable()
export class TodayClassService {

  // Repository를 주입받아 DB 조회를 위임
  constructor(
    private readonly todayClassRepo: TodayClassRepository,
  ) {}

  // DB에서 "과목1,과목2,과목3" 형태의 문자열을 ["과목1", "과목2", "과목3"] 배열로 분리하는 유틸
  // GROUP_CONCAT으로 합쳐진 문자열을 다시 쪼개는 용도
  private splitCommaText(text: string | null | undefined): string[] {
    if (!text) return [];  // null이나 빈 값이면 빈 배열 반환
    return text
      .split(",")           // 쉼표로 쪼개기
      .map((v) => v.trim()) // 각 항목의 앞뒤 공백 제거
      .filter((v) => v.length > 0); // 빈 문자열 제거
  }

  async getTodayClass(
    spaceId: number,
    date: string,
  ): Promise<TodayClassResponseDto> {

    // Promise.all: 두 DB 쿼리를 동시에(병렬로) 실행해서 속도를 높임
    // 순서대로 실행하면 쿼리1 + 쿼리2 시간이 걸리지만,
    // Promise.all은 max(쿼리1, 쿼리2) 시간만 걸림
    const [classroomRows, blockRows] = await Promise.all([
      // 이 학원의 강의실 목록 조회
      this.todayClassRepo.findClassroomsBySpace(spaceId),
      // 이 학원의 오늘 수업 스케줄 조회 (10개 이상 테이블 JOIN)
      this.todayClassRepo.findScheduleBlocks(spaceId, date),
    ]);

    // DB row(snake_case)를 API 응답 DTO(camelCase)로 변환
    // r.id → classroomId, r.notes ?? null → null 처리
    const classrooms: ClassroomDto[] = classroomRows.map((r) => ({
      classroomId: r.id,
      name: r.name,
      capacity: r.capacity,
      notes: r.notes ?? null,  // null coalescing: undefined도 null로 통일
    }));

    // DB row를 스케줄 블록 DTO로 변환
    // subjects_text: "수학,영어,과학" → subjects: ["수학", "영어", "과학"]
    const scheduleBlocks: ScheduleBlockDto[] = blockRows.map((r) => ({
      classroomId: r.classroom_id,
      sectionId: r.section_id,
      sectionName: r.section_name,
      courseId: r.course_id,
      courseName: r.course_name,
      categoryName: r.category_name ?? null,
      gradeName: r.grade_name ?? null,
      // GROUP_CONCAT 결과를 배열로 분리
      subjects: this.splitCommaText(r.subjects_text),
      instructors: this.splitCommaText(r.instructors_text),
      startTime: r.start_time,  // "09:00" 형태
      endTime: r.end_time,      // "11:00" 형태
      courseSessionId: r.course_session_id,
      // DB에서 COUNT(*) 결과가 문자열로 올 수 있어서 Number()로 명시 변환
      attendedCount: Number(r.attended_count),
      expectedCount: Number(r.expected_count),
      classroomCapacity: r.classroom_capacity,
    }));

    // 최종 응답 객체 반환
    return { date, classrooms, scheduleBlocks };
  }
}
```

---

### 4-7. `apps/api/src/todayclass/repositories/todayclass.repository.ts`

> MySQL DB에서 오늘 수업 데이터를 꺼내오는 SQL 실행 전담.

```typescript
import { DatabaseService } from "../../database/database.service";
import { Injectable } from "@nestjs/common";

// DB row 타입 정의 — SELECT 결과가 어떤 모양인지 TypeScript에 알려줌
export interface ClassroomRow {
  id: number;
  name: string;
  capacity: number;
  notes: string | null;
}

// 스케줄 블록 한 줄의 타입 정의
// 여러 테이블을 JOIN한 결과를 하나의 interface로 표현
export interface ScheduleBlockRow {
  classroom_id: number;
  classroom_name: string;
  classroom_capacity: number;
  section_id: number;
  section_name: string;
  course_id: number;
  course_name: string;
  category_name: string | null;
  grade_name: string | null;
  subjects_text: string | null;    // GROUP_CONCAT 결과: "수학,영어"
  instructors_text: string | null; // GROUP_CONCAT 결과: "김선생,이선생"
  course_session_id: number | null;
  start_time: string;              // "09:00" 형태
  end_time: string;                // "11:00" 형태
  attended_count: number;          // 출석한 학생 수 (present + late)
  expected_count: number;          // 등록된 학생 수
}

@Injectable()
export class TodayClassRepository {

  // DatabaseService를 주입받아 raw SQL 실행에 사용
  constructor(private readonly db: DatabaseService) {}

  // 이 학원의 강의실 목록을 가져오는 단순 조회
  async findClassroomsBySpace(spaceId: number): Promise<ClassroomRow[]> {
    return this.db.query<ClassroomRow>(
      `SELECT id, name, capacity, notes
       FROM office_setting_classrooms
       WHERE space_id = ?
         AND deleted_at IS NULL  -- 삭제된 강의실 제외
       ORDER BY name ASC`,       -- 이름순 정렬
      [spaceId],                 -- ? 자리에 들어갈 파라미터 (SQL injection 방지)
    );
  }

  // 오늘 수업 스케줄 전체를 가져오는 복잡한 조회
  // 10개 이상의 테이블을 JOIN하여 한 번에 필요한 모든 데이터를 가져옴
  async findScheduleBlocks(
    spaceId: number,
    date: string,
  ): Promise<ScheduleBlockRow[]> {
    return this.db.query<ScheduleBlockRow>(
      `SELECT
         cr.id              AS classroom_id,      -- 강의실 ID
         cr.name            AS classroom_name,    -- 강의실 이름
         cr.capacity        AS classroom_capacity,-- 강의실 수용 인원
         cs.id              AS section_id,        -- 출석반 ID
         cs.name            AS section_name,      -- 출석반 이름
         c.id               AS course_id,         -- 과정 ID
         c.name             AS course_name,       -- 과정 이름
         cat.name           AS category_name,     -- 카테고리 이름 (없을 수 있음)
         g.display_name     AS grade_name,        -- 학년 이름 (없을 수 있음)

         -- 서브쿼리: 과목 목록을 쉼표로 합치기
         -- GROUP_CONCAT: ["수학", "영어"] → "수학,영어"
         (
           SELECT GROUP_CONCAT(s.name ORDER BY csu.sort_order SEPARATOR ',')
           FROM office_course_subjects csu
           JOIN office_setting_subjects s ON s.id = csu.subject_id AND s.deleted_at IS NULL
           WHERE csu.course_id = c.id
         ) AS subjects_text,

         -- 서브쿼리: 강사 목록을 쉼표로 합치기
         -- is_primary DESC: 주담당 강사가 먼저 오도록 정렬
         (
           SELECT GROUP_CONCAT(esu.display_name ORDER BY ci.is_primary DESC, ci.id ASC SEPARATOR ',')
           FROM office_course_instructors ci
           JOIN edu_space_user esu ON esu.id = ci.space_user_id
           WHERE ci.course_id = c.id
         ) AS instructors_text,

         sch.course_session_id,

         -- TIME_FORMAT: "09:00:00" → "09:00" 형태로 포맷 변환
         TIME_FORMAT(sch.start_time, '%H:%i') AS start_time,
         TIME_FORMAT(sch.end_time, '%H:%i')   AS end_time,

         -- 서브쿼리: 이 회차에 출석한 학생 수
         -- status IN ('present', 'late'): 출석 또는 지각만 카운트
         -- COALESCE: section_id가 null이면 default_section_id를 사용
         (
           SELECT COUNT(*)
           FROM office_attendance_records ar
           JOIN office_enrollments e ON e.id = ar.enrollment_id
           WHERE ar.course_session_id = sch.course_session_id
             AND e.status IN ('new', 'active')
             AND ar.status IN ('present', 'late')
             AND COALESCE(ar.section_id, e.default_section_id) = cs.id
             AND ar.classroom_id = cr.id
         ) AS attended_count,

         -- 서브쿼리: 이 출석반에 등록된 학생 수 (예상 인원)
         (
           SELECT COUNT(*)
           FROM office_enrollments e2
           WHERE e2.course_id = c.id
             AND e2.status IN ('new', 'active')
             AND e2.default_section_id = cs.id
         ) AS expected_count

       FROM office_course_schedule sch
       JOIN office_course_sections cs         ON cs.id = sch.section_id
       JOIN office_courses c                  ON c.id = cs.course_id
       LEFT JOIN office_setting_grades g      ON g.id = c.grade_id
       LEFT JOIN office_course_categories cat ON cat.id = c.category_id
       JOIN office_course_section_classrooms csc ON csc.section_id = cs.id
       JOIN office_setting_classrooms cr
         ON cr.id = csc.classroom_id AND cr.deleted_at IS NULL

       -- WHERE 조건: 오늘 날짜, 취소되지 않은, 숨겨지지 않은, 이 학원의 활성 과정
       WHERE DATE_FORMAT(sch.scheduled_date, '%Y-%m-%d') = ?
         AND sch.is_cancelled = FALSE
         AND sch.deleted_at IS NULL
         AND cs.is_hidden = FALSE
         AND c.space_id = ?
         AND c.status = 'active'

       -- 강의실 이름 오름차순, 같은 강의실 안에서는 시작 시간 오름차순
       ORDER BY cr.name ASC, sch.start_time`,
      [date, spaceId],
    );
  }
}
```

---

### 4-8. `apps/api/src/todayclass/dto/todayclass.dto.ts`

> 요청 파라미터와 응답 데이터의 모양을 TypeScript로 정의하는 파일.

```typescript
import { IsDateString, IsOptional } from "class-validator";

// GET 요청의 쿼리 파라미터 DTO
// ?date=2026-03-29 같은 형태로 들어옴
export class GetTodayClassQueryDto {
  // @IsOptional: 이 필드는 없어도 됨 (없으면 오늘 날짜 사용)
  @IsOptional()
  // @IsDateString: "2026-03-29" 형태인지 자동 검증
  @IsDateString()
  date?: string;
}

// 강의실 하나의 데이터 모양
export interface ClassroomDto {
  classroomId: number;   // 강의실 고유 ID
  name: string;          // 강의실 이름 (예: "201호")
  capacity: number;      // 수용 가능 인원
  notes: string | null;  // 메모 (없을 수도 있음)
}

// 수업 스케줄 블록 하나의 데이터 모양
// DB row를 camelCase로 변환한 최종 API 응답 형태
export interface ScheduleBlockDto {
  classroomId: number;
  sectionId: number;
  sectionName: string;
  courseId: number;
  courseName: string;
  categoryName: string | null;
  gradeName: string | null;
  subjects: string[];       // ["수학", "영어"] 배열 형태
  instructors: string[];    // ["김선생", "이선생"] 배열 형태
  startTime: string;        // "09:00"
  endTime: string;          // "11:00"
  courseSessionId: number | null;
  attendedCount: number;    // 출석한 학생 수
  expectedCount: number;    // 등록된 학생 수
  classroomCapacity: number;// 강의실 수용 인원
}

// 최종 API 응답 전체 모양
export interface TodayClassResponseDto {
  date: string;                        // 조회 날짜
  classrooms: ClassroomDto[];          // 강의실 목록
  scheduleBlocks: ScheduleBlockDto[];  // 수업 스케줄 블록 목록
}
```

---

### 4-9. `apps/api/src/app.module.ts` (관련 부분)

> 앱 전체의 모듈을 등록하는 최상위 파일.

```typescript
import { Module } from "@nestjs/common";
import { ConfigModule } from "@nestjs/config";
// ... 기타 import

// TodayClassModule을 app에 등록하기 위해 import
import { TodayClassModule } from "./todayclass/todayclass.module";
import { CourseModule } from "./course/course.module";

// 참고: SupabaseModule은 app.module.ts에 직접 등록되지 않음
// → CourseModule이 내부적으로 SupabaseModule을 import해서 씀

@Module({
  imports: [
    // ConfigModule.forRoot: .env 파일을 앱 전체에서 읽을 수 있게 설정
    // isGlobal: true → 어디서든 ConfigService 주입 가능
    ConfigModule.forRoot({ isGlobal: true }),

    // ThrottlerModule: API 요청 횟수 제한 (초당 너무 많은 요청 방어)
    // ttl: 60_000ms(1분), limit: 60회 → 1분에 최대 60번만 허용
    ThrottlerModule.forRoot([{ name: "default", ttl: 60_000, limit: 60 }]),

    // TodayClassModule: GET /spaces/:spaceId/todayclass 엔드포인트
    TodayClassModule,

    // CourseModule: 출석 기록 + SupabaseModule 포함
    CourseModule,

    // ... 기타 모듈들
  ],
  providers: [
    // JwtAuthGuard: 모든 API에 JWT 인증 적용 (전역)
    { provide: APP_GUARD, useClass: JwtAuthGuard },
    // LoggerExceptionFilter: 에러를 잡아서 로깅 (전역)
    { provide: APP_FILTER, useClass: LoggerExceptionFilter },
  ],
})
export class AppModule {}
```

---

### 4-10. `apps/web/src/lib/supabase.ts`

> 프론트엔드에서 Supabase와 연결하는 클라이언트 싱글턴.

```typescript
import { createClient } from "@supabase/supabase-js";

// createClient: Supabase 연결 객체를 생성하는 팩토리 함수
// 앱 전체에서 이 파일 하나에서만 클라이언트를 생성 (싱글턴 패턴)
// → 여러 곳에서 각각 createClient를 호출하면 불필요한 연결이 여러 개 생겨서 낭비

export const supabase = createClient(
  // import.meta.env: Vite의 환경변수 접근 방법
  // VITE_*: 이 접두사가 붙은 변수만 프론트 번들에 포함됨 (보안 규칙)
  import.meta.env.VITE_SUPABASE_URL,       // Supabase 프로젝트 주소
  import.meta.env.VITE_SUPABASE_ANON_KEY,  // 공개 키 (구독/읽기용, RLS 범위 안에서만 동작)
  // 주의: service_role key는 절대 여기 쓰면 안 됨!
  // → anon key는 RLS 정책에 의해 접근이 제한됨 (안전)
  // → service_role key는 RLS를 무시해서 모든 데이터에 접근 가능 (위험)
);
```

---

### 4-11. `apps/web/src/features/todayclass/hooks/use-todayclass.ts`

> 이 파일이 실시간 연동의 프론트엔드 핵심. Supabase 구독 + React Query 관리.

```typescript
// useEffect: 컴포넌트가 화면에 그려진 후 실행할 코드를 등록하는 React 훅
import { useEffect } from "react";

// useQuery: 데이터를 가져오고 캐시하는 React Query의 핵심 훅
// useQueryClient: 캐시를 직접 조작(무효화 등)할 때 필요한 클라이언트
import { useQuery, useQueryClient } from "@tanstack/react-query";

// 실제 API를 호출하는 함수
import { fetchTodayClass } from "../api/todayclass.api";

// 앱 전체 싱글턴 Supabase 연결 객체
import { supabase } from "@/lib/supabase";

// 쿼리 키 팩토리 — React Query 캐시를 식별하는 키를 한 곳에서 관리
// "as const": TypeScript에서 이 배열의 타입을 리터럴로 고정 (타입 추론 정확도 향상)
const todayClassKeys = {
  all: ["todayclass"] as const,
  // byDate: ["todayclass", 123, "2026-03-29"] 형태의 키를 생성
  // spaceId나 date가 바뀌면 자동으로 새로 fetch함
  byDate: (spaceId: number, date: string) =>
    [...todayClassKeys.all, spaceId, date] as const,
};

// spaceId: 어느 학원의 대시보드인지
// date: 어떤 날짜의 수업인지 ("2026-03-29")
export function useTodayClass(spaceId: number, date: string) {

  // React Query 캐시를 직접 조작하기 위한 클라이언트 인스턴스
  const queryClient = useQueryClient();

  // useEffect: 컴포넌트 마운트 시 Supabase 구독을 시작하고
  // 언마운트 시 구독을 해제하는 사이드이펙트 등록
  useEffect(() => {
    // spaceId가 0 이하이면 구독하지 않음 (유효하지 않은 학원 ID 방어)
    if (spaceId <= 0) return;

    // channel: Supabase Realtime 구독의 연결 단위
    // 나중에 removeChannel()로 구독 해제할 때 필요해서 변수에 저장
    const channel = supabase
      // "attendance-signals": 채널 이름 (임의 식별자, 고유하면 됨)
      .channel("attendance-signals")
      // .on(): "이런 이벤트가 오면 이 함수를 실행해줘" 라고 등록
      .on(
        // "postgres_changes": Postgres 테이블 변경을 구독하는 이벤트 타입
        "postgres_changes",
        {
          event: "*",                          // INSERT, UPDATE, DELETE 모두 감지
          schema: "public",                    // Supabase 기본 스키마
          table: "attendance_signals",         // 감지할 테이블
          filter: `space_id=eq.${spaceId}`,   // 우리 학원 행만! (다른 학원 이벤트 제외)
        },
        // 이벤트 도착 시 실행되는 콜백 함수
        () => {
          // queryClient.invalidateQueries: 이 키의 캐시를 "오래됐어" 라고 표시
          // → 표시하는 순간 fetchTodayClass가 자동으로 다시 호출됨
          // [...todayClassKeys.all, spaceId]: ["todayclass", spaceId]
          // → spaceId가 같은 모든 날짜 캐시를 한 번에 무효화
          queryClient.invalidateQueries({ queryKey: [...todayClassKeys.all, spaceId] });
        },
      )
      .subscribe((status) => {
        // status: "SUBSCRIBING" → "SUBSCRIBED" 순서로 변화
        if (status === "SUBSCRIBED") {
          // 구독 완료 시 한 번 강제 갱신
          // → 대시보드를 열었을 때 구독 전에 변경된 데이터가 있을 수 있어서
          queryClient.invalidateQueries({ queryKey: [...todayClassKeys.all, spaceId] });
        }
      });

    // useEffect의 return 함수 = 클린업 함수
    // 컴포넌트가 사라질 때(언마운트) 또는 spaceId가 바뀔 때 실행됨
    // supabase.removeChannel: 구독 해제 → 메모리 누수 방지
    return () => { supabase.removeChannel(channel); };

  // 의존성 배열: 이 안의 값이 바뀔 때마다 useEffect를 다시 실행
  // spaceId 바뀜 → 기존 구독 해제 → 새 spaceId로 구독 재시작
  // queryClient는 앱 생애주기 동안 바뀌지 않지만 린트 규칙상 명시 필요
  }, [spaceId, queryClient]);

  // useQuery: 실제 대시보드 데이터를 서버에서 가져오는 부분
  return useQuery({
    // queryKey: 캐시 식별자. 이 배열의 값이 바뀌면 자동으로 새 데이터를 fetch
    queryKey: todayClassKeys.byDate(spaceId, date),

    // queryFn: 실제 API를 호출하는 함수
    // queryKey 변경 또는 invalidateQueries 호출 시 실행됨
    queryFn: () => fetchTodayClass(spaceId, date),

    // enabled: false이면 queryFn을 아예 실행하지 않음
    // spaceId와 date가 모두 유효할 때만 API 호출
    enabled: spaceId > 0 && date.length > 0,
  });
}
```

---

### 4-12. `apps/web/src/features/todayclass/api/todayclass.api.ts`

> 백엔드 API를 실제로 호출하는 함수.

```typescript
// authApi: JWT 인증 토큰을 자동으로 헤더에 붙여주는 axios 인스턴스
// → 로그인 상태에서만 API를 호출할 수 있음
import { authApi } from "@/lib/api/auth";

// 백엔드 DTO와 1:1로 매칭되는 TypeScript 타입
import type { TodayClassResponse } from "../types";

// spaceId: 어느 학원인지
// date: 어떤 날짜인지 ("2026-03-29")
// Promise<TodayClassResponse>: 비동기 함수, 완료 시 TodayClassResponse 반환
export async function fetchTodayClass(
  spaceId: number,
  date: string,
): Promise<TodayClassResponse> {

  // authApi.get: GET 요청을 백엔드로 보냄
  // `/spaces/${spaceId}/todayclass`: URL 경로 (예: /spaces/123/todayclass)
  // { params: { date } }: ?date=2026-03-29 형태로 쿼리 파라미터 추가
  const { data } = await authApi.get<TodayClassResponse>(
    `/spaces/${spaceId}/todayclass`,
    { params: { date } },
  );

  // data: 백엔드가 반환한 { date, classrooms, scheduleBlocks } 객체
  return data;
}
```

---

### 4-13. `apps/web/src/features/todayclass/types/index.ts`

> 백엔드 응답 데이터의 모양을 TypeScript로 정의. 백엔드 DTO와 1:1 매칭.

```typescript
// 강의실 하나의 데이터 모양
// 백엔드 ClassroomDto와 동일한 구조 (필드명, 타입 모두 일치해야 함)
export interface ClassroomDto {
  classroomId: number;
  name: string;
  capacity: number;
  notes: string | null;  // null 가능 → TypeScript가 null 처리 강제
}

// 수업 스케줄 블록 하나의 데이터 모양
export interface ScheduleBlockDto {
  classroomId: number;
  sectionId: number;
  sectionName: string;
  courseId: number;
  courseName: string;
  categoryName: string | null;
  gradeName: string | null;
  subjects: string[];       // 과목 배열 ["수학", "영어"]
  instructors: string[];    // 강사 배열 ["김선생"]
  startTime: string;        // "09:00"
  endTime: string;          // "11:00"
  courseSessionId: number | null;
  attendedCount: number;
  expectedCount: number;
  classroomCapacity: number;
}

// 백엔드 API 전체 응답의 모양
// fetchTodayClass 함수가 이 타입으로 응답을 받아서
// TypeScript가 잘못된 필드 접근을 컴파일 에러로 잡아줌
export interface TodayClassResponse {
  date: string;
  classrooms: ClassroomDto[];
  scheduleBlocks: ScheduleBlockDto[];
}
```

---

## 5. Supabase 사전 설정 (수동 1회 작업)

실시간 기능이 작동하려면 Supabase 콘솔에서 아래를 미리 설정해야 해요.

```sql
-- 1. 테이블 생성
-- attendance_signals: 출석 변경 시 신호를 보내는 용도의 전용 테이블
-- 학원마다 행이 딱 1개 (space_id가 PRIMARY KEY)
CREATE TABLE attendance_signals (
  space_id  integer PRIMARY KEY,     -- 학원 ID (중복 없음)
  pinged_at timestamptz DEFAULT now() -- 마지막 출석 변경 시각
);

-- 2. RLS(보안 정책) 활성화
-- RLS: Row Level Security — 행 단위로 접근을 제어하는 기능
-- 켜면 정책이 없는 한 아무것도 읽거나 쓸 수 없음
ALTER TABLE attendance_signals ENABLE ROW LEVEL SECURITY;

-- 3. anon key 읽기 허용 정책 추가
-- Supabase Realtime이 내부적으로 SELECT를 사용하기 때문에 필요
-- 이게 없으면 postgres_changes 이벤트가 조용히 안 날아옴
CREATE POLICY "anon can read attendance_signals"
  ON attendance_signals
  FOR SELECT
  TO anon
  USING (true);  -- true: 조건 없이 모든 행 읽기 허용

-- 4. Realtime 활성화
-- 이 명령이 없으면 테이블 변경이 있어도 이벤트가 발생하지 않음
ALTER PUBLICATION supabase_realtime ADD TABLE attendance_signals;
```

---

## 6. 환경 변수 설정

### 백엔드 (`apps/api/.env`)

```env
SUPABASE_URL=https://xxx.supabase.co        # Supabase 프로젝트 주소
SUPABASE_SERVICE_ROLE_KEY=eyJ...            # 백엔드 전용 비밀 키 (절대 프론트에 노출 금지)
```

### 프론트엔드 (`apps/web/.env`)

```env
VITE_SUPABASE_URL=https://xxx.supabase.co   # Supabase 프로젝트 주소
VITE_SUPABASE_ANON_KEY=eyJ...              # 공개 키 (RLS 범위 안에서만 동작)
```

> `VITE_` 접두사: Vite가 빌드 시 이 변수를 번들에 포함시킴.  
> `service_role key`는 절대 `VITE_`로 시작하면 안 됨 → 프론트 코드에 노출됨.

---

## 7. 처음부터 끝까지 한 번에 보기

```
[선생님이 출석 버튼 클릭]
         │
         ▼
[attendance.service.ts]
  ① attendanceRepo.upsertAttendanceRecord() → MySQL DB 저장
  ② attendanceAutoSendService.sendIfEnabled() → 문자 발송 (비동기, 결과 무관)
  ③ supabaseService.signalAttendanceUpdated(spaceId) 호출
         │
         ▼
[supabase.service.ts]
  attendance_signals 테이블 UPSERT
  { space_id: 123, pinged_at: "2026-03-29T10:30:00Z" }
  → 이전에 123번 행이 있으면 pinged_at만 UPDATE
  → 없으면 새 행 INSERT
         │
         ▼
[Supabase Realtime (중계소)]
  attendance_signals 테이블 변경 감지
  → "space_id=123 구독 중인 브라우저들에게 이벤트 전송"
         │
         ▼
[use-todayclass.ts (브라우저)]
  postgres_changes 이벤트 수신
  → queryClient.invalidateQueries(['todayclass', 123])
  → React Query가 "캐시가 오래됐다" 판단
         │
         ▼
[todayclass.api.ts]
  GET /spaces/123/todayclass?date=2026-03-29 호출
         │
         ▼
[todayclass.controller.ts → service.ts → repository.ts]
  MySQL DB에서 최신 출석 데이터 조회 (10개+ 테이블 JOIN)
  응답 반환
         │
         ▼
[TodayClassPage.tsx]
  새 데이터로 화면 자동 갱신!
  새로고침 없이도 출석 현황이 반영됨
```

---

## 8. 리소스 사용량 정리

| 이벤트 | 발생 횟수 | 영향 |
|---|---|---|
| Supabase UPSERT | 출석 1건마다 1번 | 매우 가벼움 |
| Supabase Realtime 이벤트 | UPSERT 1번마다 1개 | 구독 중인 브라우저에만 전달 |
| 백엔드 API 재호출 | 이벤트 1개마다 1번 | JOIN 쿼리, 인덱스 타면 빠름 |
| WebSocket 연결 | 대시보드 열린 동안 유지 | 탭 닫으면 자동 해제 |

학원 특성상 출석 기록은 **분당 수 건 수준**이라 Supabase Free Plan으로도 충분.

---

## 9. 핵심 개념 정리

| 개념 | 한 줄 설명 |
|---|---|
| `UPSERT` | UPDATE + INSERT. 있으면 UPDATE, 없으면 INSERT |
| `SELECT FOR UPDATE` | 행에 잠금을 걸어서 동시에 두 명이 수정 못 하게 막음 |
| `RLS` | 테이블 접근을 정책으로 통제. 켜면 정책 없이는 아무것도 안 됨 |
| `Realtime` | Supabase가 테이블 변경을 실시간으로 구독자에게 전달 |
| `postgres_changes` | Supabase Realtime의 구독 방식. INSERT/UPDATE/DELETE 감지 |
| `invalidateQueries` | React Query 캐시를 "오래됐어"로 표시 → 자동 refetch 트리거 |
| `싱글턴` | 앱 전체에서 하나의 인스턴스만 사용. `supabase.ts`가 대표 예시 |
| `DI (의존성 주입)` | NestJS가 필요한 객체를 알아서 만들어서 constructor에 넣어줌 |
| `anon key` | 프론트용 공개 키. RLS 범위 안에서만 동작. 번들에 포함돼도 안전 |
| `service_role key` | 백엔드 전용 비밀 키. RLS 무시. 절대 프론트에 노출 금지 |

---

> **한 줄 요약:**  
> "선생님이 출석을 기록하면 → NestJS가 Supabase 테이블의 시각을 업데이트하고
> → Supabase가 그 변경을 대시보드 브라우저에 실시간으로 전달해서
> → 대시보드가 자동으로 MySQL에서 최신 데이터를 다시 불러와 화면을 갱신한다."