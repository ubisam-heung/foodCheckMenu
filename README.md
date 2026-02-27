# 체크푸드메뉴 (CheckFoodMenu)

## 소개

체크푸드메뉴는 유비샘의 단골 점심 식당 식단표 이미지를 자동으로 수집하여, 누구나 쉽게 웹에서 확인할 수 있도록 만든 오픈소스 프로젝트입니다. GitHub Actions를 활용해 매일 자동으로 이미지를 업데이트하며, Vue 기반의 반응형 웹 UI로 다양한 기기에서 편리하게 식단을 확인할 수 있습니다.

## 주요 기능
- 매일 자동으로 식단 이미지 수집 및 업데이트 (GitHub Actions)
- 날짜별 식단 이미지 조회 및 이전/다음 날짜 이동
- 반응형 웹 디자인 (PC/모바일 모두 지원)
- 고정 헤더/푸터, 푸터 아이콘 버튼 및 외부 링크
- GitHub Pages를 통한 무료 공개 배포

## 사용 방법

### 1. 프로젝트 클론
```bash
git clone https://github.com/본인계정/레포명.git
cd 레포명
```

### 2. 의존성 설치
```bash
npm install
```

### 3. 개발 서버 실행
```bash
npm run dev
```

### 4. GitHub Actions 및 Pages 설정
1. 저장소의 Settings > Pages에서 배포 브랜치(main)와 폴더(dist)를 선택합니다.
2. .github/workflows/fetch_menu_image.yml 워크플로우가 매일 자동으로 식단 이미지를 수집하고, 빌드 후 Pages로 배포합니다.

### 5. 사이트 접속
설정이 완료되면, 저장소의 Pages URL(예: https://본인계정.github.io/레포명)로 접속해 식단표를 확인할 수 있습니다.

## 폴더 구조
```
├── public/           # 정적 파일 및 식단 이미지 저장
├── src/              # Vue 소스 코드
│   ├── components/   # Vue 컴포넌트
│   ├── plugins/      # 플러그인 설정
│   └── styles/       # CSS 스타일
├── .github/workflows # GitHub Actions 워크플로우
├── fetch_menu_image.py # 식단 이미지 수집 파이썬 스크립트
├── package.json      # 프로젝트 설정
└── ...
```

## 주의사항
- dist 폴더는 git에 커밋하지 않고, Actions가 빌드 후 자동 배포합니다.
- public 폴더는 .gitignore에 포함되어 있지 않아야 이미지가 정상적으로 커밋/배포됩니다.
- GitHub Actions가 정상 동작하려면 워크플로우 파일이 .github/workflows/에 있어야 합니다.

## 라이선스
MIT License

---