# Thinking in SwiftUI - 2장 State and Binding

Created: 2024년 5월 26일 오후 7:47
Tags: SwiftUI, iOS

이전 장에서 SwiftUI code가 **View tree**라는 청사진(블루프린트) 로 구성되는 방법과 영구 **Render tree**로 변환되는 방법에 대해서 알아보았습니다. 이번 장에서는 상태 기반으로 View tree를 구성하고 Render tree를 업데이트 하는 방법을 살펴봅니다.

일반적으로 뷰의 업데이트 주기는 다음과 같습니다.

1. 상태를 기반으로 View Tree가 구성됩니다.
2. 현재 View Tree를 기반으로 Render Tree가 노드를 생성, 제거, 업데이트 합니다.
3. 이벤트가 발생해 상태가 변경됩니다.
4. 1번부터 3번까지 반복합니다.

SwiftUI가 상태를 지속적으로 관찰하고 있기 때문에 언제 View tree가 다시 생성되는지, Render tree가 업데이트 되는지, 뷰의 무엇을 업데이트 해야 하는지 걱정할 필요가 없습니다. 다만, 너무 지나치게 광범위한 View 업데이트는 성능 이슈가 발생할 수 있고, 이번 장의 뒷 부분에서 다시 알아보겠습니다.

SwiftUI의 핵심이라고 할 수 있는 **Property Wrapper**에 대한 내용입니다.

```
프로퍼티 래퍼는 속성에 적용되는 래퍼(Wrapper)로, 속성의 값에 추가적인 로직을 적용하거나, 값이 변경될 때 다른 동작을 수행할 수 있도록 해준다.
```

- **@State, @Binding, @StateObject, @ObservedObject, @EnvironmentObject** 등

## **Data Flow Through SwiftUI**

---

- [https://wlaxhrl.tistory.com/91](https://wlaxhrl.tistory.com/91)

(Data Flow Through SwiftUI)

**(여기서 중요한건 SSOT !!)**

### **@State**

---

**뷰의 상태를 관리하기 위한 프로퍼티 래퍼.**

- Value Type
- 뷰의 로컬 데이터 (내부 프로퍼티)
- 뷰에서 소유되고 관리되어야 하는 데이터 (ex. 텍스트필드, 토글버튼 등)

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled.png)

Counter 예시를 살펴보면, 버튼을 누를 때마다 상태값이 변경되고 화면이 다시 그려집니다. 만약 버튼의 라벨에 상태값을 바인딩하지 않았다면, SwiftUI는 업데이트할 필요가 없다는 것을 인지하고 화면을 다시 그리지 않습니다.

## View의 생성 4단계

---

1. Counter 구조체가 처음 생성되면, View tree는 만들어지지만 아직 Render tree에 노드가 존재하지 않습니다. State라는 PropertyWrapper 역시 초기값을 할당하고 있지만, 아직 아무것도 바인딩하지 않았기 떄문에 View는 비어있습니다.

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled%201.png)

1. SwiftUI는 Render tree에 노드를 생성하면서 State를 할당합니다. 이제 PropertyWrapper 의 메모리는 랜더 노드를 가리키게 됩니다.

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled%202.png)

1. View의 body 부분이 실행되고, `Button`이 생성됩니다. 이제 state 값은 랜더 노드를 가리키고 있기 때문에 `Button` 의 label 값은 랜더 노드에 저장된 값을 사용합니다.

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled%203.png)

1. 마지막으로 노드의 값을 읽어 값이 설정된 view body 부분을 랜더링해 실제 UI를 만듭니다.

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled%204.png)

## 이벤트 발생 3단계

---

1. View에 이벤트가 발생하면 뷰와 연결된 랜더 트리에 전달되고, 랜더 트리를 지켜보고 있던 PropertyWrapper 쪽에 메모리가 증가합니다.
2. State가 변경되었기 때문에 body가 다시 실행되고, View tree 가 구성됩니다.
3. 다시 구성된 View tree를 기반으로 랜더트리의 값이 변경되고, UI가 다시 랜더링됩니다.

(ex) **SwiftUI 프레임워크의 Button의 highlight 상태는 Button 내부에서 @State로 관리된다.** 이는 터치 중일 때는 highlighted 상태로, 터치가 끝났을 때는 highlighted가 아닌 상태로 관리될 수 있기 때문에, **외부에서 관리할 필요 없이 Button 내부에서만 관리**하면 된다.

> 원래 @State property wrapper는 value type에만 사용했지만, iOS 17에서 Observable 매크로가 도입되면서 변경되었다. 하지만, 17 이전 OS에서는 value 타입에만 사용해야 합니다.
> 

## **State and Observable**

---

@State를 사용할 때 2가지 실수를 저지를 수 있습니다.

1. 외부에서 전달받은 객체를 사용하는 경우
2. View 전용 객체인데, @State를 사용하지 않는 경우

둘 다 객체의 수명과 관련이 있습니다. 외부에서 수명이 관리되는 객체의 경우 @State를 사용하지 않는다는 것 입니다.

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled%205.png)

만약, 위와 같이 모델을 외부에서 전달받는 경우 초기값은 Button에 잘 셋팅되겠지만, 이미 View가 만들어진 상태에서 외부에서 Model의 값을 변경해도 상태 변화에 영향을 주지 못합니다.

## **ObservableObject Protocol**

---

iOS 17 이후에는 @Obserable 매크로를 사용해 편하게 사용할 수 있지만, 17 이전에는 다양안 **ObservableObject Protocol** 의 속성 래퍼는 사용할 수 있습니다.

1. @StateObject
    1. @State와 거의 동일한 방식으로 동작
    2. 랜더 트리에 노드가 생성될 때 초기값을 지정합니다.
    3. @State와 동일하게 private하게 사용해야 합니다. (외부에서  전답하거나, 조작하지 말것)
2. @ObservableObject
    1. @StateObject 보다 간단한 구조로 초기값을 할당하지 않고 구독한 하는 관계

## **@ObservableObject**

---

- Reference Type
- 이미 관리(소유)하고 있는 데이터에 적용하면 좋음
- 외부로부터의 데이터를 표현할 때

case 1 : State 로 int 값을 표현할 때

```swift
struct ContentView: View {
    @State private var rootCount: Int = 0
    var body: some View {
        CountView(rootCount: rootCount)
        Button(action: {rootCount += 1}, label: {
            Text("Root Add")
        })
    }
}
```

case 2 : ObservedObject 로 모델을 표현할 때

```swift
struct CountView: View {
    @ObservedObject var viewModel = CountViewModel()
    let rootCount: Int
    var body: some View {
        VStack {
            Text("Root: \(rootCount)")
            Text("Count: \(viewModel.count)")
            Button(action: {viewModel.addCount()}, label: {
                Text("Counter Add")
            })
        }
    }
}
```

![](https://miro.medium.com/v2/resize:fit:302/1*6QE-DMrqDVycvuFBx0sp4g.gif)

Root Add 버튼을 누를 때마다 ViewModel이 초기화되고 있었다. 그러니까 Count가 0부터 새롭게 시작하게 된다.

> ViewModel이 View에 붙어있기 때문에 root add 버튼을 누르면 뷰가 새로 만들어지면서 ViewModel 도 교체된다.
> 

### **@StateObject**

> A state object behaves like an observed object, except that SwiftUI knows to create and manage a single object instance for a given view instance, regardless of how many times it recreates the view.
> 

StateObject는 ObservedObject와 거의 똑같으나, 이 StateObject는 하나의 객체로 만들어지고, View가 얼마나 초기화되든지 상관없이 별개의 객체로 관리된다.

```swift
struct CountView: View {
    @StateObject var viewModel = CountViewModel()
    let rootCount: Int
    var body: some View {
        VStack {
            Text("Root: \(rootCount)")
            Text("Count: \(viewModel.count)")
            Button(action: {viewModel.addCount()}, label: {
                Text("Counter Add")
            })
        }
    }
}
```

![](https://miro.medium.com/v2/resize:fit:302/1*8Kw64zPUp4mu4KmVMzo6fg.gif)

Root Add를 눌러도 Count가 초기화되지 않는다! 기존의 데이터가 보존되는 것을 확인할 수 있다.

### StateObject vs ObservedObject

애플이 추천하는 StateObject와 ObservedObject의 사용법은 Observable Object를 처음 초기화할 때는 StateObject를 사용하고, 이미 객체화된 것을 넘겨 받을 때 ObservedObject의 사용을 추천하고 있다. 

```swift
// 직접 View에서 만들 때
struct UpperView: View {
  @StateObject var viewModel: ViewModel = ViewModel()
  var body: some View {
    LowerView(viewModel: viewModel)
  }
}
// 외부에서 넘겨받을 때
struct LowerView: View {
  @ObservedObject var viewModel: ViewModel
  var body: some View {
    Text("Hello")
  }
}
```

**@StateObject**와 **@ObservedObject**는 각각의 생명주기와 사용법을 살펴보자.

1. **@StateObject**:
    - **생명주기**: **@StateObject**는 뷰가 생성될 때 인스턴스를 만들고, 뷰가 소멸될 때 인스턴스를 해제합니다. 뷰의 생명주기와 일치하며, 뷰가 인스턴스를 소유하고 관리합니다.
    - **사용법**: 주로 뷰 내에서 상태를 유지해야 하는 경우에 사용됩니다. 예를 들어, 뷰 내에서 데이터를 수정하고 해당 변경 사항을 추적해야 할 때 유용합니다.
2. **@ObservedObject**:
    - **생명주기**: **@ObservedObject**는 뷰가 생성될 때마다 새로운 인스턴스를 만듭니다. 뷰의 생명주기와는 독립적으로 동작하며, 뷰가 인스턴스를 소유하지 않습니다. 따라서 뷰가 인스턴스를 생성하고 해제하지 않습니다.
    - **사용법**: 다른 뷰에서 관찰하고 싶은 객체의 변경 사항을 감지할 때 사용됩니다. 주로 다른 뷰에서 생성한 인스턴스를 참조하고 싶을 때 유용합니다.

간단히 말하면, **@StateObject**는 뷰가 인스턴스를 소유하고 관리하며, **@ObservedObject**는 뷰가 인스턴스를 생성하지 않고 변경 사항을 감지할 때 사용됩니다. 이를 이해하면 SwiftUI에서 상태 관리를 더 효율적으로 할 수 있습니다!

## Update, View Performance

---

앞서 본 것과 같이 State와 UI가 연결되어 자동으로 업데이트 된다. 상태가 변경된다고 전체 UI를 다시 그리는게 아니라, 특정 State와 View 사이에 종속성을 설정해 그 부분만 업데이트 되게 된다.

SwiftUI는 일부 State가 변경 될 때 View Tree에서 꼭 필요한 부분만 다시 랜더링되도록 많은 노력을 기울인다. 그러니 이런 노력을 방해하지 않는 방식으로 코드를 작성하는 것도 중요하다.

1. 예를 들어 모든 State를 하나의 큰 객체 안에 넣는다면, 특정 변경으로 모든 하위의 작은 뷰를 업데이트 할 수 있다. 따라서 State를 작은 단위로 나눠서 뷰를 업데이트 하는게 성능적으로 더 도움이됩니다.
2. 실제로 필요한 값만 하위 View로 전달하는게 중요합니다. 많은 데이터를 가진 큰 객체가 있고, 이 객체를 통으로 넘겨주게 되면, 객체가 업데이트 될 때 마다 객체가 업데이트 될 수 있습니다.

성능 이슈가 발생할 때 어떤 뷰의 body가 실행되는지 판단하는 몇가지 방법이 있습니다.

### 1. print 삽입

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled%206.png)

### 2. Self.printCahnges()

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled%207.png)

print문과 다르게 재실행된 이유를 같이 호출해줍니다.

- 상태 변경으로 다시 호출되는 경우 ⇒ 상태 이름, 속성 표시
- 뷰 값 자체가 변경된 경우 ⇒ 속성이 변경된 경우 @self가 기록됩니다.
- View의 ID 값이 변경된 경우 ⇒ @identity가 기록됩니다. (일반적으로 새로 삽입된 경우)

### 3. instruments

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled%208.png)

### **Observable 매크로**

---

[Observation](https://developer.apple.com/documentation/Observation)을 통해 SwiftUI는 observable data model 에 의존성을 형성하고 data 가 변할때마다 UI 를 업데이트 합니다.

### **기존 ObservableObject 와 달라지는 것들**

**첫번째: 코드가 간결해짐**

| **AS-IS** | **TO-BE** |
| --- | --- |
| final class Book: ObservableObject {
    @Published var title = "Sample Book Title"
    var isAvailable = true
}

struct BookView: View {
    @ObservedObject var book: Book
    
    var body: some View {
        Text(book.title)
    }
} | @Observable final class Book {
    var title = "Sample Book Title"
    var isAvailable = true
}

struct BookView: View {
    var book: Book
    
    var body: some View {
        Text(book.title)
    }
} |

**두번째: 뷰 업데이트 매커니즘이 좀 더 효율적으로 바뀜**

@Observable 매크로를 쓰면

뷰의 body 에서 프로퍼티를 직접 읽어야지만 뷰 업데이트가 된다.

ObservableObject에서는 published 프로퍼티가 변하면 뷰가 해당 프로퍼티를 읽고 있지 않아도 다시 그려진다.

**세번째: data model object 를 optional로 들고 있을 수 있다.**

**네번째: data model objects를 collection으로도 가능하다.**

[**https://eunjin3786.tistory.com/580**](https://eunjin3786.tistory.com/580)

![Untitled](Thinking%20in%20SwiftUI%20-%202%E1%84%8C%E1%85%A1%E1%86%BC%20State%20and%20Binding%207dc1b55d26f948b49c6257b6bfbabd18/Untitled%209.png)

- 매크로 기능은 iOS 17 이상

새로운 매크로 기반 객체 관찰 모델은 **편리한 구문**을 도입하고, 뷰와 관찰 가능한 객체 간의 종속성이 형성되는 방식을 변경합니다. 이전 속성 래퍼를 사용할 때, SwiftUI는 `@StateObject`의 `objectWillChange` 게시자를 맹목적으로 구독하거나, `@ObservedObject`를 뷰에서 선언했습니다.

새로운 `Observable` 매크로를 사용하면, `Observable`의 모든 속성이 뷰 본문에서 접근하는 객체는 객체가 어디에서 왔는지에 관계없이 이 뷰에 대한 종속성을 형성합니다.

**이 새로운 모델은 훨씬 더 간결하고 효율적입니다.** 예를 들어, 뷰 본문에서 전역 **싱글톤(관찰 가능)**에 액세스할 경우, `@ObservedObject`를 사용하여 싱글톤을 뷰에 전달할 필요 없이, 액세스된 속성과 뷰 사이에 자동으로 종속성이 형성됩니다. 관찰 가능한 객체는 옵션, 배열 또는 다른 컬렉션에 중첩될 수 있으며, 속성 수준 추적으로 인해 관찰 및 뷰 업데이트가 예상대로 계속 작동합니다.

또한, 뷰 본문에서 객체의 속성 하나만 사용하는 경우, 다른 속성이 변경되어도 이 뷰는 다시 그려지지 않습니다. 모델 객체를 사용하지 않는 경우(예: 코드의 한 분기에만 존재하는 경우), 모델은 전혀 관찰되지 않습니다. 이를 통해 불필요한 뷰 업데이트를 줄여 성능을 향상시킬 수 있습니다. 이전에는 모델 객체를 수동으로 분할하여 더 세분화된 뷰 업데이트를 얻었습니다.