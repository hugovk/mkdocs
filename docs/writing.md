# Writing Markdown

MkDocs supports regular Markdown syntax with some Github Flavored Markdown extensions.

For other references on writing in Markdown, see the [GitHub documentation](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax), the [Markdown Guide](https://www.markdownguide.org/), or the author's [original documentation](https://daringfireball.net/projects/markdown/).

The rest of this page provides a reference guide to the supported markdown syntax.

## Headings

```markdown
# H1
## H2
### H3
#### H4
##### H5
```

<h1>H1</h1>
<h2>H2</h2>
<h3>H3</h3>
<h4>H4</h4>
<h5>H5</h5>

## Formatting

```markdown
* **Bold text**
* *Italic text*
* ~~Strikethrough~~
* <ins>Underlined</ins>
* e <sup>i π</sup> = -1
* H<sub>2</sub>O
```

<span></span>

* **Bold text**
* *Italic text*
* ~~Strikethrough~~
* <ins>Underlined</ins>
* e <sup>i π</sup> = -1
* H<sub>2</sub>O

## Lists

```markdown
- First item
- Second item
- Third item
```

<span></span>

- First item
- Second item
- Third item

## Ordered Lists

```markdown
1. First item
2. Second item
3. Third item
```

<span></span>

1. First item
2. Second item
3. Third item

## Links

```markdown
See [wikipedia](https://www.wikipedia.org/).
```

See [wikipedia](https://www.wikipedia.org/).

## Section links

```markdown
See the [Links](#links) section.
```

See the [Links](#links) section.

## Relative Links

```markdown
Back to the [Homepage](index.md).
```

Back to the [Homepage](index.md).

## Images

```markdown
![coder cat](img/codercat.png)
```

![coder cat](img/codercat.png)

## Inline Code

```markdown
`&mdash;`
```

`&mdash;`

## Code Block

<pre><code class="language-markdown hljs">```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```</code></pre>

<span></span>

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```

## Horizontal Rule

```markdown
---
```

---

<br/>

## Table

```markdown
| Syntax    | Description |
| --------- | ----------- |
| Header    | Title       |
| Paragraph | Text        |
```

<span></span>

| Syntax    | Description |
| --------- | ----------- |
| Header    | Title       |
| Paragraph | Text        |

## Footnotes

```markdown
Here's a sentence with a footnote. [^1]

[^1]: This is the footnote from earlier.
```

Here's a sentence with a footnote. [^1]

[^1]: This is the footnote from earlier.

## Blockquote

```markdown
> Rumors of my death have been greatly exaggerated.
```

> Rumors of my death have been greatly exaggerated.

## Alerts

```markdown
> [!NOTE]
> Useful information that users should know, even when skimming content.
```

> [!NOTE]
> Useful information that users should know, even when skimming content.

```markdown
> [!TIP]
> Helpful advice for doing things better or more easily.
```

> [!TIP]
> Helpful advice for doing things better or more easily.

```markdown
> [!IMPORTANT]
> Key information users need to know to achieve their goal.
```

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

```markdown
> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.
```

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

```markdown
> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
```

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.

## Emoji

```markdown
:+1: This PR looks great :heart:
```

:+1: This PR looks great :heart:

## Task List

```markdown
- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media
```

<span></span>

- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media
