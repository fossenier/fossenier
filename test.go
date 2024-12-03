package main

type data int

// constructor
// func MakeNull() IList

type IList interface {
	// mutators
	Cons(d data) IList // prepend
	Snoc(d data) IList // append

	// predicates
	IsNull() bool

	// operations
	Len() int

	// accessors
	//   data invariant: only allowed for non-null lists
	Car() data  // [0], first
	Cdr() IList // [1:], rest
}

type Null struct{}

type Cell struct {
	d    data
	next IList
}

func (n Null) Cons(d data) IList {
	return Cell{d, n}
}

func (n Cell) Cons(d data) IList {
	return Cell{d, n}
}

func (n Null) Snoc(d data) IList {
	return Cell{d, n}
}

func (n Cell) Snoc(d data) IList {
	return Cell{n.d, n.Snoc(d)}
}

func (_ Null) IsNull() bool {
	return true
}

func (_ Cell) IsNull() bool {
	return false
}

func (_ Null) Len() int {
	return 0
}

func (n Cell) Len() int {
	return 1 + n.next.Len()
}

func (n Null) Car() data {
	panic("Null.Car")
}

func (n Cell) Car() data {
	return n.d
}

func (n Null) Cdr() IList {
	panic("Null.Cdr")
}

func (n Cell) Cdr() IList {
	return n.next
}

func MakeNull() IList {
	return Null{}
}

// Imperative

type Tag int

const (
	NullTag = iota
	CellTag
)

type List struct {
	tag  Tag
	d    data
	next *List
}

func (l List) Cons(d data) *List {
	return &List{CellTag, d, &l}
}

func (l List) Snoc(d data) *List {
	switch l.tag {
	case NullTag:
		return &List{NullTag, d, &l}
	case CellTag:
		return &List{CellTag, l.d, l.next.Snoc(d)}
	default:
		panic("List.Snoc")
	}
}





// predicate-logic predicate HEAPREC(n) means
// 	data(n) < data(left(n)) $$ data(n) < data(right(n))
// 	&& HEAPREC(left(h))     && HEAPREC(right(h))

// and t being a heap HEAP(t) means HEAPREC(root(t))

func (t node) IsHeap() bool, bool, int // is heap, is valid data, value {
	lh, lv, ld = IsHeap(t.left)
	rh, rv, rd = IsHeap(t.right)
	// no valid data? no need for comparison
	// Make sure that left is less than right
}