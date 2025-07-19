# Thinking in SwiftUI - 1장 View Trees

Created: 2024년 5월 26일 오후 6:23
Tags: SwiftUI, iOS

뷰 트리와 렌더 트리는 SwiftUI 작업을 이해하는 데 있어 가장 기본적이고 중요한 개념입니다. 원하는 레이아웃을 얻기 위해서는 뷰 트리의 구성 방식을 이해해야 합니다.

상태가 어떻게 작동하는지 이해하려면, SwiftUI에서 뷰의 수명과 그것이 만들고 있는 뷰 트리와의 관계를 이해하는 것이 중요합니다. 이를 이해하면, 데이터를 효율적으로 로드하고 필요할 때 뷰를 업데이트하는 SwiftUI 코드를 작성하는 데 도움이 됩니다.

마지막으로, 애니메이션과 전환이 어떻게 작동하는지 이해하려면 뷰 트리에 대한 이해가 필요합니다.

- 뷰 트리
- 뷰 수명
- 애니메이션 전환

## **View Tree와 Render Tree**

---

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled.png)

위와 같은 코드를 작성하면, 중앙에 일시적인 청사진이 구축되며, 이를 'View Tree'라고 합니다. 그 결과, 왼쪽처럼 View가 렌더링되어 보여집니다.

뷰 트리를 살펴보면, 트리는 역순으로 그려집니다. '`background`'는 트리의 최상단에 위치하지만, 실제로는 아무것도 그리지 않고, '`Text`' 뒤쪽에 위치하게 됩니다.

- `View Tree`: 일시적인 인스턴스로 뷰를 구성하는 청사진

만약, 아래와 같이 순서를 변경하게 된다면

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%201.png)

`background`는 `padding`의 자식이 되며, `Text`에 `background`이 붙게 됩니다. 그러면 `background`에 `padding`이 붙어서 다음과 같은 모습이 됩니다.

## **ViewBuilders**

---

SwiftUI는 '**뷰 빌더(ViewBuilder)**'라는 특별한 구문을 이용해 뷰 목록을 구성합니다. 뷰 빌더는 이 목적을 위해 Swift 언어에 추가된 결과 빌더 기능을 기반으로 만들어졌습니다. 예를 들어, 이미지를 텍스트 옆에 표시하는 뷰를 구성하는 방법은 다음과 같습니다.

(뷰 빌더는 `ResultBuilder` 피처의 위에 구현되었다)

- [https://minsone.github.io/swift-resultbuilder](https://minsone.github.io/swift-resultbuilder)
- [https://github.com/apple/swift-evolution/blob/main/proposals/0289-result-builders.md](https://github.com/apple/swift-evolution/blob/main/proposals/0289-result-builders.md)

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%202.png)

**`HStack`**은 클로저를 매개변수로 사용하며, 이 클로저는 **`@ViewBuilder`**로 표시됩니다. 이를 통해 내부에 여러 표현식을 작성할 수 있으며, 각 표현식은 뷰를 나타냅니다. 본질적으로 스택에 전달된 클로저는 이 예제에서 스택의 하위 뷰가 되는 뷰 목록을 생성합니다.

```swift
extension ViewBuilder {
public static func buildBlock<C0, C1>(_ c0: C0, _ c1: C1) ->
    TupleView<(C0, C1)> where C0 : View, C1 : View
}
```

위 예제의 스택에는 내부에 **두 개의 뷰 표현식**이 있으므로 두 개의 매개변수가 있는 뷰 빌더의 **`buildBlock`** 메소드가 호 출됩니다. 반환 유형에서 볼 수 있듯이 이는 이미지와 텍스트라는 두 가지 보기를 래핑하는 **`TupleView`**를 구성합니다. 뷰 빌더 를 뷰 목록을 나타내는 **`TupleView`**를 구성하는 메커니즘으로 생각할 수 있습니다.

**하위 뷰를 구성하는 뷰 컴포넌트** (암시적으로 `@ViewBuilder`로 표시)

- 스택, 그리드 등과 같은 **모든 컨테이너 뷰**
- `background`, `overlay`..

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%203.png)

- [https://zeddios.tistory.com/m/1366](https://zeddios.tistory.com/m/1366)

## **Dynamic Content (동적 컨텐츠)**

---

SwiftUI 코드를 작성하고 ViewBuilder를 통해서 View 목록을 작성하는데, 이 때 View 목록도 동적일 수 있습니다. if - else 구문을 통해서 뷰를 동적으로 구성하는 방법은 아래와 같습니다.

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%204.png)

if 문 대신, if let, switch 문도 사용 가능합니다.

## Render Trees

---

View Tree는 일시적으로 만들어지는 청사진의 역할을 하는 반면에, Render Tree는 더 긴 수명으로 계속 머무르다가 상태가 바뀌면 현재 상태를 반영하도록 업데이트 하는 역할을 합니다.

랜더 트리는 SwiftUI 내부에 존재하기 때문에, 직접 다룰일은 없습니다. 하지만, SwiftUI의 동작을 이해하는데 유용한 모델입니다.

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%205.png)

만약 옵셔널한 View 구조가 있다면, View Tree에서는 다음과 같이 생성됩니다.

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%206.png)

하지만, Render Tree의 경우에는 다릅니다. Text가 nil일 경우 View Tree가 Render Tree를 만들 땐 실제로 View에 대응되도록 HStack 안에 Image 하나만 존재합니다.

만약에 State가 업데이트되서 View 업데이트가 동작하게 된다면, Render Tree에 Text가 삽입되거나, 제거됩니다. (하지만, Text의 문구가 변경어도 Text View가 새로 만들어지는 건 아닙니다.)

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%207.png)

## LifeTime

---

위에서 언급했듯이 View Tree는 일시적인 청사진의 역할을 합니다. 따라서 View의 수명(Life Time)과는 관계가 없습니다. 하지만 Render Tree는 처음 랜더링 된 시점부터 View가 더 이상 표시되지 않을 때 까지 수명을 가집니다. 다만, Render Treedml 수명은 화면상의 UI와 동일하지 않습니다. 

만약, 스크롤 뷰 안에 큰 VStack이 있고 많은 View를 랜더링하는 경우 화면에 View가 보이는 여뷰랑 상관없이 모든 VStack의 하위 뷰 노드가 만들어집니다.

VStack은 LazyStack과 달리 바로 바쁘게 랜더링을 시작합니다. 그렇다고 LazyStack을 사용한다고 바로 바로 화면에서 보이지 않는다고 해제되는 건 아닙니다. 생성되는 시점이 늦어질 뿐 화면을 벗어나도 Render 노드가 유지됩니다. 

(자세한 내용은 상태(State)에 대한 파트에서 다룰 예정입니다. 중요한건 렌더 트리의 노드를 통제할 수 없다는 것 입니다.)

SwiftUI에서는 실용적인 사용을 위해서 View의 LifeTime을 체크할 수 있도록 3가지 인터페이스 터널을 제공합니다.

1. onAppear
    1. 뷰가 화면에 나타날 때마다 실행됩니다. Render Tree의 노드가 생산될 때 호출되는게 아니라, View가 화면에 노출될 때마다 실행되기 때문에 여러번 호출할 수 있습니다. 예를들어서 LazyVStack 또는 List의 뷰가 스크롤을 통해 화면 밖으로 나갔다가 다시 돌아올 경우에도 매번 onAppear가 호출됩니다.
    2. TabView에서 탭을 전환할 때 역시 매번 호출됩니다.
2. onDisappear
    1. 화면에서 뷰가 사라질 때 호출됩니다. onAppear와 동일한 규칙으로 여러번 호출될 수 있습니다.
3. task
    1. 비동기 작업에 사용되는 onAppear와 onDisappear 두가지의 조합입니다. 이 task modifier는 onAppear가 호출되는 시점에 작업을 생성하고, onDisappear가 호출되는 시점에 작업을 취소합니다.

View의 id가 유지되는 동안은 값이 변경되어도 SwiftUI 관점에서의 View는 동일합니다.

State, ObservedObject는 View의 id와 연결된 저장소입니다. View의 lifetime 동안 body가 재계산되더라도 저장소의 메모리를 유지합니다.

View의 id가 변경되면 새로운 View로 간주되며 이전 View는 메모리에서 해제됩니다.

SwiftUI에서 View의 lifetime과 State의 lifetime은 동일한 의미를 갖습니다.

## **Identity (식별성)**

---

만약 작성한 코드에서 View의 ID값을 할당하지 않는다면, View Tree에서 생성될 View마다 고유 ID 값을 할당합니다. 이렇게 자동으로 할당되는 ID를 암시적 ID라 합니다. 이 ID 값을 통해서 뷰를 식별할 수 있고 ID가 동일할 경우 View를 새로 만드는게 아닌, 상태값을 업데이트 합니다.

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%208.png)

특이한 부분은 if else  브랜치에서 1이라는 동일한 ID 값 아래에 다른 ID값을 가진다는 것 입니다. 따라서 동일한 양쪽 다 동일한 Text를 사용하고 있지만, 다른 ID값을 가지고 있어 condition이 변경되면 새로 View를 만들어 추가하게 됩니다.

View Tree에서의 암시적인 ID 할당이 아닌, 명시적으로 ID 값을 할당할 수도 있습니다. 주로 ForEach를 통해 반복적인 View를 생성하고 해당 View의 상태를 업데이트 하기 위해서 명시적으로 ID를 지정합니다.

ID는 Hashable 값을 사용할 수 있습니다.

아래의 경우 true, false 값을 ID로 사용해 2개의 Text를 번갈아 추가 삭제 할 수 있습니다.

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%209.png)

- Explicit id는 **`.id(_:)`** 메서드를 사용하여 명시적으로 지정할 수 있습니다.

그렇다면, 다음과 같이 하나의 Text를 만들어서 2번 사용하는 경우 ID값이 어떻게 될까?

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%2010.png)

View Tree에 표시된 것 처럼 다른 위치에 있기 때문에 View Tree에서 서로 다른 암시적인 ID값을 할당하고 별도의 뷰로 간주됩니다. 이 부분 때문에 View Tree를 청사진이라 생각할 수 있는 것 입니다.

다음으로 만약에 이런 condition에 따라 분기하는 applayIf 를 만들고 적용하면 어떻게 될까?

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%2011.png)

적용한 코드 샘플을 보면 if else 형태로 하이라이트가 들어가면 background 모디파이어를 추가하는 형태로 구현하고 View Tree 역시 if else 형태와 유사한 모습을 보이고 있다.

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%2012.png)

이 경우 동일하게 Text는 변함이 없지만, 불필요하게 2개의 Text가 condition에 따라서 생성, 제거되는 모습을 볼 수 있다. 이런 패턴이 아닌 아래와 같은 패턴을 사용하는게 좋다.

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%2013.png)

이 경우 if else 의 값에 따라서 상태값을 변경해 랜더 노드를 추가, 삭제하지 않는다.

## View의 Life Time 단계

---

### 1. Appearing

1. 스테이트 구독 (State, **ObservedObject**)
2. body 계산, 스테이트 연결
3. body 처음 호출
4. **뷰 그래프** 업데이트, UI 그리기
5. **onAppear는 top-down으로 실행됨**

### 2. Updating

1. 스테이트 변경 또는 publisher 구독으로 유저 액션 발생
2. 이전 스냅샷과 뷰 계층 비교
3. 변경된 뷰를 무력화한다
4. 뷰 그래프 업데이트하고 무력화된 뷰를 그림. 모든 업데이트 플로우는 뷰 계층을 타고 내려옴

### 3. Disappearing

1. 뷰 계층에서 제거되고 호출. top-down으로 실행
2. View가 화면에서 사라질 때 발생합니다.
3. 이 단계에서는 View의 정리(clean-up) 작업이 이루어집니다.
4. 예를 들어, **`onDisappear`** modifier를 사용하여 Disappearing 단계에서 리소스를 해제하거나 데이터를 저장할 수 있습니다.

[https://www.vadimbulavin.com/swiftui-view-lifecycle/](https://www.vadimbulavin.com/swiftui-view-lifecycle/)

![Untitled](Thinking%20in%20SwiftUI%20-%201%E1%84%8C%E1%85%A1%E1%86%BC%20View%20Trees%20f3167e10922a4ad2978ce336fd5ddb62/Untitled%2014.png)