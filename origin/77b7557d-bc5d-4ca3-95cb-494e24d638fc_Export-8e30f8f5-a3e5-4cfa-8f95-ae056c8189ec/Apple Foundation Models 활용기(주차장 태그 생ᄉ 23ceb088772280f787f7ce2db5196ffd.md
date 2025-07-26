# Apple Foundation Models 활용기(주차장 태그 생성)

표지: Apple%20Foundation%20Models%20%E1%84%92%E1%85%AA%E1%86%AF%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%80%E1%85%B5(%E1%84%8C%E1%85%AE%E1%84%8E%E1%85%A1%E1%84%8C%E1%85%A1%E1%86%BC%20%E1%84%90%E1%85%A2%E1%84%80%E1%85%B3%20%E1%84%89%E1%85%A2%E1%86%BC%E1%84%89%2023ceb088772280f787f7ce2db5196ffd/2025-07-26_20-48-50.png
상태: 작성 중
Tags: iOS
작성일: 2025/07/26

## 온디바이스 AI, 새로운 가능성의 문을 열다: Apple Foundation Models 활용기

WWDC25에서 공개된 **Apple Foundation Models**는 클라이언트 개발자들에게 혁신적인 온디바이스(On-device) AI의 시대를 예고했습니다. 클라우드 기반 AI 서비스가 범람하는 가운데, 기기 자체에서 AI 모델 추론이 이뤄진다는 것은 **강력한 개인 정보 보호, 지연 없는 실시간 응답, 그리고 안정적인 오프라인 기능**이라는 새로운 가능성을 제시합니다.

저 또한 이러한 새로운 패러다임에 대한 기대를 안고, Foundation Models를 직접 테스트해보기 위해 간단한 토이 프로젝트를 만들었습니다.

![Jul-26-2025 20-01-18.gif](Apple%20Foundation%20Models%20%E1%84%92%E1%85%AA%E1%86%AF%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%80%E1%85%B5(%E1%84%8C%E1%85%AE%E1%84%8E%E1%85%A1%E1%84%8C%E1%85%A1%E1%86%BC%20%E1%84%90%E1%85%A2%E1%84%80%E1%85%B3%20%E1%84%89%E1%85%A2%E1%86%BC%E1%84%89%2023ceb088772280f787f7ce2db5196ffd/Jul-26-2025_20-01-18.gif)

### 🧪 테스트 환경 및 프로젝트 개요

- **하드웨어:** Apple M1 16GB
- **운영체제:** macOS 16.0 베타 (25A5316i)

> 이 프로젝트는 **MapKit**을 활용하여 사용자 주변의 주차장 정보를 조회하고, 지도에 핀을 표시하는 기본적인 앱으로 시작했습니다. 기능 구현의 많은 부분은 **Gemini**의 도움을 받아 빠르게 진행할 수 있었습니다. 여기에 핵심적으로 **Foundation Models**를 적용하여 각 주차장의 특징을 나타내는 **태그를 자동으로 생성**하는 기능을 추가했습니다.
> 

## 💡 Foundation Models 적용: 주차장 태그 자동 생성

태그 생성은 `LanguageModelSession`을 통해 이뤄집니다. 특정 주차장의 이름, 카테고리, 주소 등의 정보를 프롬프트로 구성하여 모델에 전달하고, 핵심 특징을 담은 태그를 요청하는 방식입니다.

```jsx
var session = LanguageModelSession(instructions: "MKMapItem 정보로 주차장 태그를 생성")

let name = mapItem.name ?? "정보 없음"
let category = mapItem.pointOfInterestCategory?.rawValue ?? "정보 없음"
let address = mapItem.address?.fullAddress ?? "정보 없음"

let prompt = """
    다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
    예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전

    ---
    [주차장 정보]
    이름: \(name)
    카테고리: \(category)
    주소: \(address)
    """
    
do {
    let response = try await session.respond(to: prompt, generating: Tags.self)
    // ... 시간 로깅 및 결과 반환 ...
} catch {
    // ... 에러 처리 ...
}
```

### 겪었던 도전과 해결 과정

새로운 기술을 도입하는 과정은 언제나 예측하지 못한 난관과 마주하게 됩니다. Foundation Models도 예외는 아니었습니다.

### 1. `LanguageModelSession`의 동시성 제약: `respond(to:)` 중복 호출 문제

가장 먼저 맞닥뜨린 문제는 모델 파싱과 함께 태그를 생성하려고 했을 때 발생한 에러였습니다. 여러 주차장에 대해 동시에 태그 생성을 요청하자 다음과 같은 메시지가 콘솔을 가득 채웠습니다.

```jsx
Attempted to call respond(to:) a second time before the model finished responding to the previous prompt. 
You should observe the isResponding property on LanguageModelSession and wait until it becomes false before submitting another prompt.
```

이는 `LanguageModelSession`이 한 번에 하나의 프롬프트 요청만 처리할 수 있다는 명확한 경고였습니다. 모델이 이전 응답을 완료하기 전에 다음 요청을 보내려 했기 때문에 발생한 문제였습니다.

**해결:** 이 문제를 해결하기 위해, 태그 생성 로직을 담당하는 UseCase인 `DefaultGenerateParkingTagsUseCase`를 `actor`로 변경했습니다. `actor`는 Swift Concurrency에서 동시성 문제를 안전하게 다룰 수 있도록 돕는 구조입니다. 또한, `session.isResponding` 속성을 주기적으로 확인하여 모델이 이전 응답을 완료할 때까지 기다리는 방어적인 로직을 추가했습니다.

```jsx
actor DefaultGenerateParkingTagsUseCase: GenerateParkingTagsUseCase {
    // ...
    func execute(mapItem: MKMapItem) async throws -> [String] {
        while session.isResponding {
            try await Task.sleep(nanoseconds: 100_000_000)  // 100ms 대기 (안정성 강화)
        }
        // ... 프롬프트 전송 ...
    }
    // ...
}
```

이제 `actor`의 직렬화된 실행과 `isResponding`을 통한 명시적인 대기 덕분에, `LanguageModelSession`은 안전하게 한 번에 하나의 요청만 처리하게 되었습니다.

## 2. 컨텍스트 윈도우 초과 에러: `exceededContextWindowSize`

동시성 문제를 해결한 후에도 `Fatal error`와 함께 **`exceededContextWindowSize`** 에러가 간헐적으로 발생했습니다. 이는 모델에게 전달하는 프롬프트의 길이가 모델이 한 번에 처리할 수 있는 최대 **컨텍스트 윈도우**를 초과했음을 의미합니다. 특히 한국어 텍스트는 영어에 비해 동일한 문자열 길이라도 더 많은 토큰을 차지하는 경향이 있어, 컨텍스트 윈도우 한계에 더 빨리 도달할 수 있습니다.

- **`LanguageModelSession.GenerationError.exceededContextWindowSize`**

**해결:** 다행히 이 에러는 WWDC 영상에서도 언급되었던 부분이었습니다. 이 에러가 발생했을 때 **`LanguageModelSession`을 새롭게 초기화**하고 프롬프트 요청을 재시도하는 로직을 추가했습니다.

```jsx
// ...
catch LanguageModelSession.GenerationError.exceededContextWindowSize {
    // ... 로깅 ...
    session = newSession(previousSession: session) // 새 세션 생성
    return (try? await response(to: prompt)) ?? [] // 재시도
}
// ...

private func newSession(previousSession: LanguageModelSession) -> LanguageModelSession {
    // 트랜스크립트의 첫/마지막만 보존하여 컨텍스트 압축 (예시)
    let entries = [
        previousSession.transcript.first, previousSession.transcript.last,
    ].compactMap { $0 }
    let condensedTranscript = Transcript(entries: entries)
    return LanguageModelSession(transcript: condensedTranscript)
}
```

- WWDC 영상에서도 첫번째(프롬프트)와 마지막(가장 최근 답변) 을 압축

프롬프트 내용을 최대한 간결하게 줄이는 노력과 함께 이 재시도 로직을 적용하자, 해당 에러는 더 이상 발생하지 않았습니다. 이는 **프롬프트 최적화**와 **적절한 에러 핸들링**이 Foundation Models 사용에 있어 필수적임을 보여줍니다.

### 3. 성능 최적화: 병렬 태그 생성의 필요성

앞선 과정을 통해 기능은 안정화되었지만, 성능 문제가 대두되었습니다. 14개의 주차장 항목에 대한 태그 생성을 직렬로 처리했을 때, **평균 5.56초** (로그 기준)라는 시간이 소요되었습니다. 이는 모바일 앱의 사용자 경험 관점에서 매우 긴 시간입니다.

`LanguageModelSession`이 마치 거대한 DB 모델처럼 느껴져 단일 인스턴스로 직렬 처리해야 한다고 생각했으나, 그보다는 **OS의 AI 엔진에 대한 질의 세션**에 가깝다는 결론에 도달했습니다. 즉, `LanguageModelSession` 인스턴스 자체가 무거운 리소스가 아니며, 여러 인스턴스를 생성하여 병렬로 사용하는 것이 가능하다는 의미였습니다.

**해결:** 각 태그 생성을 **독립적인 `Task`로 분리하고, 각 `Task`에서 고유한 `DefaultGenerateParkingTagsUseCase` 인스턴스를 생성하여 사용**하도록 구조를 변경했습니다.

```jsx
// MARK: Tag 조회
func getTagByParkingInfo(_ parkingInfo: ParkingInfo) async -> [String] {
  let useCase = DefaultGenerateParkingTagsUseCase()
  return (try? await useCase.execute(parkingInfo: parkingInfo)) ?? []
}
```

놀랍게도, 이 접근 방식을 적용하자 **명시적인 에러 메시지 없이** 태그 생성이 훨씬 빠르게 진행되기 시작했습니다. 이는 여러 `LanguageModelSession` 인스턴스가 각자의 스레드 또는 Concurrency 환경에서 병렬적으로 모델 추론을 요청할 수 있음을 시사합니다.

### 맺음말: 온디바이스 AI의 현재와 미래

Apple Foundation Models는 온디바이스 AI의 강력한 가능성을 제시하지만, 현재 베타 단계에서는 몇 가지 주의사항을 요구합니다.

- **동시성 관리:** `LanguageModelSession`의 직렬 처리 제약을 이해하고 `actor`와 `isResponding` 폴링으로 안전하게 다루는 것이 중요합니다.
- **프롬프트 최적화:** 컨텍스트 윈도우 한계를 고려하여 프롬프트를 간결하게 유지해야 합니다.
- **성능 최적화:** 필요하다면 여러 `LanguageModelSession` 인스턴스를 병렬로 사용하여 사용자 경험을 개선할 수 있습니다.
- **디버깅 및 피드백:** 상세한 로깅과 Apple Feedback Assistant를 통한 피드백은 개발 과정에서 큰 도움이 됩니다.

제가 경험한 것처럼, 온디바이스 AI는 여전히 발전 중인 분야이며, 그 활용에는 섬세한 접근이 필요합니다. 하지만 기기 자체에서 강력한 AI 기능을 구현할 수 있다는 점은 분명 모바일 앱 개발에 새로운 혁신을 가져올 것입니다. 앞으로 Foundation Models가 더욱 성숙해져, 개발자들이 더 쉽고 강력하게 온디바이스 AI를 활용할 수 있기를 기대합니다.

![image.png](Apple%20Foundation%20Models%20%E1%84%92%E1%85%AA%E1%86%AF%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%80%E1%85%B5(%E1%84%8C%E1%85%AE%E1%84%8E%E1%85%A1%E1%84%8C%E1%85%A1%E1%86%BC%20%E1%84%90%E1%85%A2%E1%84%80%E1%85%B3%20%E1%84%89%E1%85%A2%E1%86%BC%E1%84%89%2023ceb088772280f787f7ce2db5196ffd/image.png)

Git: https://github.com/Leejigun/FoundationModels_ParkingLot

## 관련 코드

```jsx
protocol GenerateParkingTagsUseCase {
    func execute(mapItem: MKMapItem) async throws -> [String]
    func execute(parkingInfo: ParkingInfo) async throws -> [String]
}

@Generable(description: "주차장 특성 태그")
struct Tags {
    @Guide(description: "MKMapItem 기반으로 주차장의 특징을 태그로 생성")
    public let tags: [String]
}

actor DefaultGenerateParkingTagsUseCase: GenerateParkingTagsUseCase {

    var session = LanguageModelSession(instructions: "MKMapItem 정보로 주차장 태그를 생성")

    func execute(mapItem: MKMapItem) async throws -> [String] {
        while session.isResponding {
            try await Task.sleep(nanoseconds: 100_000_000)  // 대기 시간 100ms로 늘려 안정성 강화
        }

        let name = mapItem.name ?? "정보 없음"
        let category = mapItem.pointOfInterestCategory?.rawValue ?? "정보 없음"
        let address = mapItem.address?.fullAddress ?? "정보 없음"

        let prompt = """
            다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
            예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전

            ---
            [주차장 정보]
            이름: \(name)
            카테고리: \(category)
            주소: \(address)
            """
        return try await response(to: prompt)
    }

    func execute(parkingInfo: ParkingInfo) async throws -> [String] {
        while session.isResponding {
            try await Task.sleep(nanoseconds: 100_000_000)  // 대기 시간 100ms로 늘려 안정성 강화
        }

        let name = parkingInfo.name
        let distance = parkingInfo.distance ?? "정보없음"
        let address = parkingInfo.address ?? "정보없음"

        let prompt = """
            다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
            예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

            ---
            [주차장 정보]
            이름: \(name)
            거리: \(distance)
            주소: \(address)
            """
        return try await response(to: prompt)
    }

    private func response(to prompt: String) async throws -> [String] {
        let startTime = Date()
        do {
            let response = try await session.respond(
                to: prompt,
                generating: Tags.self
            )
            
            let timeElapsed = Date().timeIntervalSince(startTime)
            print(
                "DEBUG: Model responded in \(String(format: "%.2f", timeElapsed)) seconds for prompt:\n\(prompt)\n- \(response.content.tags)\n"
            )
            
            return response.content.tags
        } catch LanguageModelSession.GenerationError.exceededContextWindowSize {
            
            let timeElapsed = Date().timeIntervalSince(startTime)
            print(
                "DEBUG: Model exceeded context window in \(String(format: "%.2f", timeElapsed)) seconds for prompt:\n\(prompt)\n- exceededContextWindowSize\n"
            )
            
            session = newSession(previousSession: session)
            return (try? await response(to: prompt)) ?? []
        } catch {
            
            let timeElapsed = Date().timeIntervalSince(startTime)
            print(
                "DEBUG: Model exceeded context window in \(String(format: "%.2f", timeElapsed)) seconds for prompt:\n\(prompt)\n- \(error.localizedDescription)\n"
            )
            
            return []
        }
    }

    private func newSession(previousSession: LanguageModelSession)
        -> LanguageModelSession
    {
        let entries = [
            previousSession.transcript.first, previousSession.transcript.last,
        ].compactMap { $0 }
        let condensedTranscript = Transcript(entries: entries)
        return LanguageModelSession(transcript: condensedTranscript)
    }
}
```

## 디버그 로그

```jsx
DEBUG: Model responded in 3.68 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 수양유료주차장
거리: 755.565m
주소: 대한민국 서울특별시 은평구 불광동 13-5, 03360
- ["#유료주차장", "#넓은주차장", "#서울주차장", "#은평구주차장", "#서울특별시주차장"]

DEBUG: Model responded in 4.63 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 연신내유료주차장
거리: 501.125m
주소: 대한민국 서울특별시 은평구 불광동 81-8, 03338
- ["#유료", "#연신내", "#서울", "#주차장"]

DEBUG: Model responded in 5.75 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 연광초등학교지하공동주차장
거리: 877.267m
주소: 대한민국 서울특별시 은평구 연서로35길 37, 03342
- ["지하주차장", "공영", "연광초등학교", "서울특별시", "은평구"]

DEBUG: Model responded in 7.26 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 불광2동거주자우선주차장
거리: 725.101m
주소: 대한민국 서울특별시 은평구 불광동 131-4, 03347
- ["#지하주차장", "#공영주차장", "#서울특별시주차장", "#은평구주차장", "#주거지역주차장"]

DEBUG: Model responded in 8.03 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 연신중학교
거리: 754.294m
주소: 대한민국 서울특별시 은평구 연서로33길 16-32, 03342
- ["#학교주차장", "#서울특별시", "#은평구", "#연신중학교"]

DEBUG: Model responded in 1.60 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 새장골공영주차장
거리: 883.138m
주소: 대한민국 서울특별시 은평구 불광동 480-352, 03340
- ["#공영", "#무료", "#넓은", "#지하주차장", "#서울특별시"]

DEBUG: Model responded in 3.48 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 불광2동거주자우선주차장
거리: 725.101m
주소: 대한민국 서울특별시 은평구 불광동 131-4, 03347
- ["#주거지우선주차장", "#지하주차장", "#서울특별시", "#은평구"]

DEBUG: Model responded in 4.63 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 수양유료주차장
거리: 755.565m
주소: 대한민국 서울특별시 은평구 불광동 13-5, 03360
- ["유료", "넓은", "서울", "주차장", "주차"]

DEBUG: Model responded in 5.68 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 연신중학교
거리: 754.294m
주소: 대한민국 서울특별시 은평구 연서로33길 16-32, 03342
- ["#근처", "#연신중학교", "#서울특별시"]

DEBUG: Model responded in 6.71 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 연신내유료주차장
거리: 501.125m
주소: 대한민국 서울특별시 은평구 불광동 81-8, 03338
- ["#유료", "#넓은", "#지하주차장", "#서울", "#은평"]

DEBUG: Model responded in 8.22 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 연광초등학교지하공동주차장
거리: 877.267m
주소: 대한민국 서울특별시 은평구 연서로35길 37, 03342
- ["지하주차장", "학교주차장", "서울주차장", "근처주차장", "공영주차장"]

DEBUG: Model responded in 7.21 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 새장골공영주차장
거리: 883.138m
주소: 대한민국 서울특별시 은평구 불광동 480-352, 03340
- ["#공영", "#무료", "#지하주차장", "#서울특별시", "#은평구"]

DEBUG: Model responded in 7.19 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 연신내유료주차장
거리: 501.125m
주소: 대한민국 서울특별시 은평구 불광동 81-8, 03338
- ["#유료", "#공영", "#넓은", "#지하주차장", "#서울특별시"]

DEBUG: Model responded in 3.75 seconds for prompt:
다음 주차장 정보에서 가장 핵심적인 특징을 나타내는 태그를 5개 이내로 생성해줘.
예시 태그: #24시간, #공영, #무료, #넓은, #지하주차장, #야외주차장, #마트주차장, #병원주차장, #쇼핑몰주차장, #식당주차장, #공항주차장, #역주차장, #환승주차장, #전기차충전, #가까운, #먼

---
[주차장 정보]
이름: 새장골공영주차장
거리: 883.138m
주소: 대한민국 서울특별시 은평구 불광동 480-352, 03340
- ["#공영", "#무료", "#지하주차장", "#서울특별시", "#은평구"]
```