# svc
**Separated Values Compression** is a compression algorithm specifically for files with separated values, the most common form of this is Comma Separated Values (`.csv`) but some files are delimited with other symbols.

# Idea
Suppose we have a data file that has two columns. The first column is a uniform distrobution of letters A, B, C, or D. Then the second column is a uniform distrobution of numbers 1, 2, 3, or 4. Now we want to use Huffman coding to compress this file, here is what the tree would look like. 

```mermaid
graph TB
    A(( ))-- 0 -->B(( ))
    A-- 1 -->C(( ))
    B-- 0 -->D(( ))
    B-- 1 -->E(( ))
    C-- 0 -->F(( ))
    C-- 1 -->G(( ))
    D-- 0 -->H((A))
    D-- 1 -->I((B))
    E-- 0 -->J((C))
    E-- 1 -->K((D))
    F-- 0 -->L((1))
    F-- 1 -->M((2))
    G-- 0 -->N((3))
    G-- 1 -->O((4))
```

Which would result in a compression table like the following.
| Symbol   | Bit String |
|----------|----------|
| A        | `000`   |
| B        | `001`   |
| C        | `010`   |
| D        | `011`   |
| 1        | `100`   |
| 2        | `101`   |
| 3        | `110`   |
| 4        | `111`   |

Here, the average length of the compressed bit string is 3, we can do better.

The main premise of **separated values compression** is that some columns use a smaller set of symbols which means that the entropy of individual columns is smaller compared to the rest of the data.

We know that the first column is always going to be a letter (A, B, C, or D) and the second column is going to be a number (1, 2, 3, or 4), so we can modify our tree to look like the following. 

```mermaid
graph TB
    A(( ))-- 0 -->B(( ))
    A-- 1 -->C(( ))
    B-- 0 -->D((A))
    B-- 1 -->E((B))
    C-- 0 -->F((C))
    C-- 1 -->G((D))
    D --> H(( ))
    E --> H
    F --> H
    G --> H
    H-- 0 --> I(( ))
    H-- 1 --> J(( ))
    I-- 0 --> K((1))
    I-- 1 --> L((2))
    J-- 0 --> M((3))
    J-- 1 --> N((4))
```

This tree would generate a compression table like the following. 
| Symbol   | Bit String |
|----------|----------|
| A        | `00`   |
| B        | `01`   |
| C        | `10`   |
| D        | `11`   |
| 1        | `00`   |
| 2        | `01`   |
| 3        | `10`   |
| 4        | `11`   |

Here, the average bit string length is 2 which results in higher compression than the original tree.