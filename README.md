A small interpreted language built from scratch in Python to learn how interpreters work.

> Work in progress. This is a learning project, so expect rough edges (see [Known limitations](#known-limitations)).

```
function add(a, b)
    jumpback a + b
end
print add(2, 3)

var total = 0
var i = 1
loop 5
    total = total + i
    i = i + 1
end
print total

var nums = [10, 20, 30]
print nums[1]
```

Output:

```
5
15
10
```

Things that make it a little different: arrays are **1-indexed**, `loop` covers both counted loops and while loops, and functions return with the `jumpback` keyword.

## Running it
Put your program in the `source_code` string in `main.py`, then run:

```
python main.py
```

## Syntax

Statements are separated by newlines, and blocks (`if`, `loop`, `function`) are closed with `end`. Indentation is ignored.

### Values

- Integers: `1`
- Booleans: `true`, `false`
- Arrays: `[1, 2, 3]`

### Variables

```
var x = 5      # declare
x = x + 1      # reassign
```

### Operators

| Kind | Operators |
| --- | --- |
| Arithmetic | `+` `-` `*` `/` |
| Comparison | `>` `<` `>=` `<=` `==` |

### Arrays

```
var nums = [10, 20, 30]
print nums[1]     # 10 (indexing starts at 1)
```

### Print

```
print x
```

### If / else

```
if x > 3
    print 1
else
    print 0
end
```

### Loops

A loop with a number repeats that many times:

```
loop 5
    print 1
end
```

A loop with a condition runs while the condition is true:

```
var n = 0
loop n < 3
    n = n + 1
end
```

### Functions

```
function add(a, b)
    jumpback a + b
end

print add(2, 3)
```

`jumpback` returns a value from a function.

## Semantics

- **Scope:** each function call gets its own scope. Functions can read globals, but assigning inside a function creates a local variable.
- **Functions** are always defined globally.
- **Undefined:** Note that the language does not report errors yet so undefined behavior may error, be stuck in an indefinite loop, silently execute, etc.

## Known limitations

This is a work in progress. Things I know about and haven't fixed yet:

- Operators inside `()` or `[]` aren't handled correctly, so `f(n - 1)` and `arr[i + 1]` misparse. 
- Nested brackets and calls (`[[1, 2], [3]]`, `a[b[1]]`, `f(g(1))`) misparse.
- Assigning to a global from inside a function creates a local instead.
- The source must end with a newline.
- Not implemented: strings, floats, parenthesized grouping, unary minus, `and` / `or`, index assignment (`arr[1] = 5`), error messages.

## How it works

Source code goes through three stages:

| Stage | File | What it does |
| --- | --- | --- |
| Tokenizer | `tokenizer.py` | Turns source text into a list of tokens |
| Parser | `parser.py` | Builds an abstract syntax tree from the tokens |
| Evaluator | `evaluator.py` | Walks the tree and runs it (tree-walking interpreter) |

Token and node type definitions live in `language_types/`. `main.py` ties the stages together.
