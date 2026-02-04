# 컴파일된 리버싱 챌린지 실행 파일들

이 폴더에는 모든 리버싱 문제의 컴파일된 .exe 파일들이 들어있습니다.

## 폴더 구조
```
compiled_executables/
├── easy/           # 쉬운 문제 10개
├── medium/         # 보통 문제 10개
├── hard/           # 어려운 문제 10개
└── README.md       # 이 파일
```

## 사용 방법
1. 각 난이도 폴더로 이동
2. .exe 파일을 실행
3. 플래그를 찾아서 입력

## 파일명 규칙
- easy 폴더: problem_01.exe ~ problem_10.exe
- medium 폴더: problem_01.exe ~ problem_10.exe  
- hard 폴더: problem_01.exe ~ problem_10.exe

## 리버싱 도구 추천
- **정적 분석**: IDA Free, Ghidra, x64dbg
- **동적 분석**: OllyDbg, x64dbg, Process Monitor
- **헥스 에디터**: HxD, 010 Editor

## 주의사항
- 모든 플래그는 `FLAG{...}` 형식입니다
- 일부 문제는 특정 입력값이 필요합니다
- 동적 분석과 정적 분석을 모두 활용하세요