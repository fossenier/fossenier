type Deque struct {
	data []int // Internal representation: slice of integers
}

// NewDeque creates and returns an empty Deque
// Specification:
// Precondition: True (no specific condition)
// Postcondition:
//   - D' = [] (the deque is initialized as empty)
//   - |D'| = 0 (the size of the deque is zero)
func NewDeque() Deque {
	return Deque{data: []int{}}
}

// PushFront adds an elemnt to the front of the Deque
// Specification:
// Precondition: D exists
// Postcondition:
//   - Front(D') = value (the new element becomes the front)
//   - D' = [value] {union} D (the element is prepended to the deque)
//   - |D'| = |D| + 1 (the size increases by 1)
func (d Deque) PushFront(value int) Deque {
	d.data = append([]int{value}, d.data...) // Prepend value
	return d
}

// PushBack adds an element to the back of teh deque
// Specification:
// Precondition: D exists
// Postcondition:
//   - Back(D') = value (the new element becomes the back)
//   - D' = D {union} [value] (the element is appended to the deque)
//   - |D'| = |D| + 1 (the size increases by 1)
func (d Deque) PushBack(value int) Deque {
	d.data = append(d.data, value) // Append value
	return d
}