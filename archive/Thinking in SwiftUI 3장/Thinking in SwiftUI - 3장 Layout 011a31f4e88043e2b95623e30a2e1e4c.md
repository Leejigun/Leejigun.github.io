# Thinking in SwiftUI - 3장 Layout

Created: 2024년 5월 26일 오후 10:51

SwiftUI의 레이아웃 알고리즘은 간단합니다. 상위 뷰는 하위 뷰에 크기를 제안하고, 하위 뷰는 그 제안에 따라 자신의 크기를 결정 후, 이 크기를 상위 뷰에 보고합니다. 그 다음 상위 뷰는 이를 자신의 좌표계 내에 배치합니다. 본질적으로, 레이아웃 프로세스의 목표는 각 뷰에 위치와 크기를 제공하는 것입니다.

가장 먼저 염두에 두어야 할 점은 SwiftUI의 레이아웃 알고리즘이 뷰 트리를 따라 **하향식으로 진행**된다는 것입니다. 그러므로 뷰 빌더 코드에 의해 생성된 뷰 트리를 이해하는 것이 중요합니다

( 이에 대한 자세한 내용은 뷰 트리 장을 참조하세요 ). 

실제 뷰 트리에 레이아웃 알고리즘을 적용하는 방법을 더 잘 이해하기 위해 예제를 살펴보겠습니다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled.png)

이 예에서 VStack은 루트 뷰이므로 안전 화면 영역을 제안된 크기로 받게 됩니다. 자체 크기를 결정하기 위해 스택은 먼저 하위 뷰에 크기를 재귀적으로 제안합니다.

 이미지는 지구본 기호의 크기를 기준으로 크기를 보고하고, 텍스트는 제안된 크기와 렌더링해야 하는 문자열을 기준으로 크기를 보고합니다. 이미지와 텍스트가 크기를 정확히 결정하는 방법에 대해 자세히 설명하겠습니다(크기는 나중에). 

이제 스택은 두 개의 하위 뷰를 서로 아래에 배치하여 둘 사이에 기본 간격을 삽입합니다. 스택은 하위 뷰 프레임의 합집합 크기로 자체 크기를 계산하고 이를 다시 창에 보고합니다.

1. 상위 뷰는 하위 뷰에 크기를 제안합니다.
2. 하위 뷰는 이 제안을 기반으로 자신의 크기를 결정하며, 자신의 하위 뷰가 있는 경우 1단계부터 다시 시작합니다.
3. 하위 뷰는 결정한 크기를 상위 뷰에 보고합니다.
4. 상위 뷰는 보고받은 크기에 따라 하위 뷰를 배치합니다.

> 3단계에서 하위 뷰에 의해 보고된 크기는 하위 뷰의 최종 크기입니다. 상위 뷰는 이 크기를 일방적으로 변경할 수 없습니다. 상위 뷰는 2단계로 돌아가 또 다른 크기 제안을 할 수 있지만, 결국 하위 뷰는 자신에게 적합한 크기를 선택하여 결정합니다.
> 

자세한 순서를 다시 보면 아래와 같습니다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%201.png)

이 예시에서는 safe area 가 320 480인 창이 있다고 가정합니다.

1. 시스템은 배경에 320 480 사이즈를 제안합니다.
2. 배경은 기본 하위 뷰에 동일한 320 480 사이즈를 제안합니다.
3. 패딩은 각 가장자리에서 10포인트를 뺀 300 460 사이즈를 텍스트에 제안합니다.
4. 텍스트는 그 크기를 51 17로 보고합니다.
5. 패딩은 각 가장자리에 10포인트를 추가하여, 크기를 71 37로 보고합니다.
6. 배경은 보조 하위 뷰(색상)에 패딩된 텍스트의 크기인 71 37을 제안합니다.
7. 색상은 제안된 71 37 사이즈를 수용하고 그대로 보고합니다.
8. 배경은 기본 하위 뷰의 크기인 71 37을 보고합니다.

## **Leaf Views**

---

### Text

기본적으로 Text 뷰는 제안된 크기에 맞게 조정됩니다. 텍스트는 이 작업을 수행하기 위해 다음 순서로 여러 전략을 사용합니다: 텍스트를 여러 줄로 나누기(단어 줄 바꿈), 단어를 나누기(줄 바꿈), 자르기, 마지막으로 텍스트를 조정하기.

텍스트는 항상 콘텐츠를 렌더링하는데 필요한 정확한 크기를 반환합니다. 이 크기는 제안된 너비보다 작거나 같고 최소한 한 줄의 높이입니다(0 제안 제외). 즉, 텍스트는 0부터 콘텐츠 전체를 렌더링하는데 필요한 크기까지 임의의 너비를 가질 수 있습니다.

다음은 Text("Hello, World!")가 제안된 크기에 따라 어떻게 렌더링되는지에 대한 몇 가지 예입니다. 점선 사각형은 제안된 크기를 나타내고, 실선 사각형은 반환된 크기를 나타냅니다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%202.png)

→ `.lineLimit(_ number:)`를 사용하면 제안된 수직 공간에 관계없이 렌더링할 최대 라인 수를 지정할 수 있습니다. nil을 지정하면 줄 제한이 없음을 의미합니다.

→ `.lineLimit(_limit:reservesSpace:)`를 사용하면 렌더링할 최대 줄 수를 지정하고, 비어 있는지 여부에 관계없이 보고된 크기에 이러한 줄의 공간을 항상 포함하는 옵션을 제공합니다.

→ `.truncationMode(_ mode:)`를 사용하면 잘림을 적용할 위치를 지정할 수 있습니다.

→ `.minimumScaleFactor(_ Factor:)`를 사용하면 제안된 크기에 맞도록 글꼴 크기를 축소할 수 있는 텍스트의 양을 지정할 수 있습니다.

만약, fixedSize()를 Text에 적용시키면, 제안과 다른 결과를 보여준다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%203.png)

### **Shapes**

대부분의 기본 제공 모양(**Rectangle**, **RoundedRectangle**, **Capsule** 및 **Ellipse**)은 0부터 무한대까지 제안된 크기를 수용하고 사용 가능한 공간을 채웁 니다. **원은 예외입니다.** 제안된 크기에 맞춰지고 원의 실제 크기를 다시 보고합니다. 모양에 nil을 제안하는 경우(즉, .fixedSize로 래핑하는 경우) 기본 크기는 10 10입니다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%204.png)

## **Colors**

`Color.red`와 같이 색상을 뷰로 직접 사용하는 경우, 레이아웃 관점에서는 `Rectangle().fill(⋯)`처럼 동작합니다.

그러나 특별한 경우가 있습니다. ignoresSafeAreaEdges에 색상을 넣으면, 해당 색상이 마법처럼 ignoresSafeAreaEdges으로 확장됩니다. 이 동작은 레이아웃에 영향을 주지 않지만, 우리 모두가 어느 시점에서 이 문제를 겪게 될 것이므로, 이를 언급하고자 했습니다. 이를 방지하기 위해서는, .background에서 ignoresSafeAreaEdges 매개변수를 사용하거나, Color 대신 Rectangle().fill(⋯)을 사용할 수 있습니다.

### **Image**

기본적으로 이미지 보기는 정적 값, 즉 기본 이미지의 크기를 보고합니다. 이미지에 대해 `.resizeable()`을 호출하면 보기가 완전히 유연해집니다. 그런 다음 이미지는 제안된 크기를 수락하고 이를 다시 보고하며 이미지를 해당 크기로 압축합니다. 실제로 크기 조 정이 가능한 거의 모든 이미지는 다음과 결합됩니다.

이미지가 왜곡되는 것을 방지하기 위한 `.aspectRatio(contentMode:)` 또는 `.scaleToFit()` modifier를 사용합니다.

### **Divider**

구분선이 수평 스택 외부에서 사용되는 경우 제안된 너비를 수락하고 구분선의 높이를 보고합니다. 수평 스택 내에서 구분 선은 제안된 높이를 승인하고 구분선의 너비를 보고합니다. **nil을 제안하면 상황에 따라 가변 축의 기본 크기가 10이 됩 니다.**

### **Spacer**

수평 또는 수직 스택 외부에서 Spacer는 **최소 길이부터 무한대까지 제안된 크기를 허용**합니다. 

수직 스택 내에서 Spacer는 최소 길이에서 무한대까지의 높이를 허용하지만 **너비 는 0으로 보고됩니다.**

스페이서의 최소 길이는 minLength를 사용하여 길이를 지정하지 않는 한 기본 패딩의 길이입니다.

## Modifier View

---

ViewModifier는 항상 다른 레이어 내부에 기존 뷰를 래핑합니다. **수정자는 적용된 뷰의 상위가 됩니다.** SwiftUI에는 ViewModifier 프로토콜을 준수하는 값을 적용하기 위한 .modifier API가 있지만 SwiftUI의 내장 수정자는 모두 View의 확장으로 노출됩니다(이는 자체 뷰 수정자에도 좋은 방법입니다). 이 섹션에서는 레이아웃에 영향을 미치는 뷰 수정자를 설명합니다.

### Frame

- 고정값 지정
- 유연하게 지정
    - 유연하게 frame 값을 설정한 경우 2번 범위를 정하게 됩니다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%205.png)

만약 다음과 같이 설정한 경우 320 480 화면에서 렌더링될 때

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%206.png)

1. 시스템은 패딩을 320, 480으로 제안합니다.

2. 패딩은 배경에 300 460을 제안합니다.

3. 배경은 기본 하위 뷰에 동일한 300 460을 제안합니다. (frame).

- 일단 가능한 최대값을 제안

4. 프레임은 하위 뷰(텍스트)에 동일한 300 460을 제안합니다.

5. 텍스트에서는 크기가 76 17이라고 보고합니다.

6. 프레임의 너비는 max(0, min( .infinity, 300)) = 300이 됩니다. 

- 0 및 .infinity 값은 유연한 프레임에 대해 지정된 인수입니다.

7. 배경은 유연한 프레임의 크기(300 17)를 제안합니다.

8. 색상은 제안된 크기를 수락하고 보고합니다. (300 17)

9. 배경은 기본 하위 뷰의 크기(300 17)를 보고합니다.

10. 패딩은 각 측면에 10포인트를 추가하고 크기를 320 37로 보고합니다.

## AspectRatio

AspectRatio 유연한 frame 사이즈로 작업할 때 유용하게 사용할 수 있습니다. 예를 들어 아래 코드는 4:3 인 직사각형을 그릴 수 있습니다.

```swift
Color.secondary
	.aspectRatio(4/3, contentMode: .fit)
```

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%207.png)

aspectRatio의 일반적으로 이미지에 사용합니다. 이미지에 .resizable() 을 붙이면 사이즈에 맞게 이미지가 늘어나거나 줄어드는데, 이미지가 깨지지 않도록 aspectRatio 를 사용해 화면 사이즈에 맞춰 이미지 사이즈를 조절할 수 있습니다.

**만약, 비율을 적용하지 않은 경우 어떻게 될까?**

aspectRatio modifier는 하위 뷰의 이상적인 크기를 제안을 통해 조사하고, 비율을 적용합니다.

만약, 이미지를 사용했을 때 이미지의 사이즈가 100:30 이라고 가정하고, 전체 사이즈가 200:200 이면, 아래와 같은 절차를 따라 사이즈를 설정합니다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%208.png)

1. AspectRatio의 크기는 200x200으로 제안을 내려보냅니다.

2. AspectRatio는 이미지에 nil x nil로 제안합니다.(사이즈 제한 없이)

3. 이미지의 이상적인 크기는 100x30으로 제안을 올려보냅니다.

4. 가로 세로 비율이 100/30인 직사각형을 200 200에 맞춥니다.

- 200 60이며 이 크기를 이미지에 제안합니다.

5. 이미지의 크기는 200 60으로 보고됩니다.
6. AspectRatio는 하위 뷰의 크기인 200 60을 자체 크기로 보고합니다.

> AspectRatio를 적용한다고 반드시 비율에 맞게 조정되는건 아닙니다. 하위뷰가 유연하지 않을 경우 적용되지 않을 수 있습니다.
> 

### **Overlay and Background**

Overlay와 Background는 SwiftUI에서 가장 유용한 수정자 중 하나입니다. 레이아웃 측면에서는 정확히 동일한 방식으로 작동합니다. 유일한 차이점은 Overlay는 기본 View 위에 보조 View를 그리는 반면, Background는 기본 View 뒤에 보조 View를 그리는 것입니다. 예를 들어, 일부 텍스트 뒤에 배경을 그리려면 다음과 같이 할 수 있습니다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%209.png)

Background와 overlay는 기본 하위 View의 레이아웃에 영향을 미치지 않습니다. 보고된 overlay 또는 background의 크기는 항상 기본 하위 View의 보고된 크기입니다.

## Container View

---

HStack과 VStack은 단순해보이지만, 결과를 파악하는데 복잡할 수 있다.

만약 아래와 같이 사이즈를 지정하지 않은 경우 제안된 크기에 따라서 다른 결과가 나온다.

```swift
HStack(spacing: 0) { 
	Color.cyan 
	Text("Hello, World!") 
	Color.teal
}
```

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%2010.png)

1. 큰 크기를 제공한 케이스 (150x50)
    1. 모두 충분한 크기를 제공받았지만, Text의 경우에는 텍스트가 들어간 경우의 사이즈가 이상적인 상한선 크기로 잡을 수 있다.
    2. 그에 비해서 Color는 유연하기 때문에 채울 수 있는 만큼 Text를 채우고 남은 공간을 Color가 나눠 가지게 된다.
2. 작은 크기를 제공한 케이스 (100x50)
    1. 3개 모두 표현하기에 충분하지 않은 사이즈가 나온 경우 3등분하게 된다. 필요에 따라서 텍스트가 줄바꿈되거나 잘리게 된다.
3. 만약 극단적으로 작은 사이즈를 준다면 (40x40)
    1. 이 경우 사이즈를 설정할 수 없기 때문에, Text가 Container의 제안을 무시하고 이상적인 사이즈로 표시해버립니다.
    2. 대안은 .layoutPriority modifier를 적용해 내부 View 사이에 우선순위를 제공하는 것 입니다.
        
        ![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%2011.png)
        

### ZStack

ZStack은 얼핏보면 overlay나 background와 동일한 역할을 할 것 같지만, overlay와 background는 ViewModifier기 때문에 하위뷰의 사이즈에 영향을 받는다. 그에 비해서 ZStack은 컨테이너기 때문에 내부의 View의 크기와 상관없이 Size를 잡게된다.

만약, 아래 코드를 root 에서 실행하게되면, 화면 전체를 다 가리게 된다.

### ScrollView

제안된 화면을 가득 채우게 되고, 내부 View는 contents의 사이즈에 맞춰진다.

```swift
ScrollView { 
	Image("logo")
		.resizable()
		.aspectRatio(.fit) 
	Text("This is a longer text")
}
```

> scrollView에 Shape 의 서브 뷰를 넣으면 10x10으로 표시되는 것을 볼 수 있다. 이는 Shape의 ProposedView의 기본값이 10, 10 이기 때문이다.
> 

### **GeometryReader**

제안받은 크기에 접근하는데 사용합니다. GeometryProxy 를 통해 제안받은 크기에 접근 할 수 있습니다.

```swift
GeometryReader { proxy in 
	Text(verbatim: "\(proxy.size)")
}
```

그러나 스택 오버플로우나 다른 사이트를 볼 때 GeometryReader에서 이슈가 생겨 고통받는 경우가 많습니다. 예를 들어서 GeometryReader 를 주위에 배치하고, Text의 사이즈를 측정하려고 하는 경우 Text 주변의 레이아웃이 잘못 나오는 경우가 많이 보고됩니다.

GeometryReader는 꼭 필요한 경우에만 써야 하고, 다음과 같은 경우에 유용하게 사용할 수 있습니다.

- GeometryReader 내부에 유연한 View를 넣는 경우 레이아웃 사이즈를 체크할 수 있습니다.
    - 예를 들어서 ScrollView 안에 GeometryReader를 넣는 경우 ScrollView의 내부 View 사이즈를 알 수 있습니다.
- background나 overlay 안에 GeometryReader를 넣으면 기본 View 크기에는 영향을 미치지 않지만 관련된 다양한 값을 읽을 수 있습니다. (고급 레이아웃 장에서 더 자세한 예를 살펴보겠습니다.)

### List

---

List는 UIkit에서 UITableView와 동일합니다. List 자체는 제안받은 크기를 가지며, ScrollView와 유사하게 View 자체는 너비와 높이를 제안하지 않습니다.

행의 높이가 고정되지 않은 UITableView와 비슷하고 내부에 배치된 항목을 기준으로 내부 View의 높이를 추정합니다.

### LazyHStack, LazyVStack

List와 동일하게 View가 보여질 때 업데이트 한다.

### LazyVGrid, LazyHGrid

LazyVGrid와 LazyHGrid는 모두 동일한 기본 알고리즘을 사용하여 열이나 행의 크기를 계산하므로 이 섹션 에서는 LazyVGrid에 중점을 둘 것입니다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%2012.png)

그리드는 iOS 16에서 추가되었고, 17 이상에서도 아직 버그가 많기 때문에 짧게 다루고 넘어간다. 

(가급적 쓰지 말것)

### **ViewThatFits**

제안된 크기에 따라 다른 보기를 표시하려면 ViewThatFits를 사용하면 됩니다. 여러 개의 하위 뷰가 필요한 경우, 제안된 크기에 맞는 첫 번째 하위 뷰를 표시합니다. 이는 각 하위 뷰의 이상적인 크기를 파악하기 위해 nil을 제안하고, 이상적인 크기가 제안된 크기 내에 맞는 첫 번째 하위 뷰(코드에 하위 뷰가 나타나는 순서대로)를 표시합니다. 적합한 하위 뷰가 없으면 마지막 하위 뷰를 선택합니다.

### **Rendering Modi!ers**

SwiftUI에는 offset, RotationEffect, scaleEffect 등과 같이 뷰의 렌더링 방식에는 영향을 주지만 레이아웃 자체에는 영향을 미치지 않는 여러 뷰 수정자가 있습니다. 이러한 수정자는 CGContext.translate와 같은 작업을 수행한다고 생각할 수 있습니다. 이는 뷰가 그려지는 위치를 변경하지만, 레이아웃 시스템에서 보면 뷰는 여전히 원래 위치에 있습니다.

## **Alignment**

기본적으로 거의 모든 뷰는 하위 뷰의 중앙에 배치됩니다.

```swift
Text("Hello")
	.frame(width: 100, height: 100) // 기본값이 .center
```

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%2013.png)

```swift
Text("Hello")
	.frame(width: 100, height: 100, alignment: .bottomTrailing)
```

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%2014.png)

정렬 가이드

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%2015.png)

ZStack 역시 기본값은 .center라 아래의 경우 가운데에 쌓이게 된다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%2016.png)

### 정렬 가이드 수정

center, bottom같은 기본 정렬 가이드라인을 수정할 수 있다.

```swift
let image = Image(systemName: "pencil.circle.!ll") 
	.alignmentGuide(.firstTextBaseline, computeValue: { dimension in
		dimension.height/2 
	}
)
```

image의 .firstTextBaseline을 줄여서 Image 가 firstTextBaseline으로 정렬했더니 아래로 밀리게 된다.

이렇게 수정한 이미지를 적용하면 다음과 같이 가이드라인이 변경된다.

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%2017.png)

하지만 firstTextBaseline 을 수정했기 때문에 center로 설정하면 바뀌는게 없다.

이를 사용해 다음과 같이 범용적으로 적용 가능한 뱃지 아이콘을 만들수도 있다.

```swift
extension View {
    func badge<B: View>(@ViewBuilder _ badge: () -> B) -> some View {
        overlay(alignment: .topTrailing) { badge()
                .alignmentGuide(.top) { $0.height/2 }
		            .alignmentGuide(.trailing) { $0.width/2 } }
    }
}
```

![Untitled](Thinking%20in%20SwiftUI%20-%203%E1%84%8C%E1%85%A1%E1%86%BC%20Layout%20011a31f4e88043e2b95623e30a2e1e4c/Untitled%2018.png)