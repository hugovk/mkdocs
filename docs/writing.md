# Writing Markdown

MkDocs deployed with Markdown, HTML & CSS.

Thanks for visiting [The Markdown Guide](https://www.markdownguide.org)!

This Markdown cheat sheet provides a quick overview of all the Markdown syntax elements. It can’t cover every edge case, so if you need more information about any of these elements, refer to the reference guides for [basic syntax](https://www.markdownguide.org/basic-syntax/) and [extended syntax](https://www.markdownguide.org/extended-syntax/).

## Basic Syntax

These are the elements outlined in John Gruber’s original design document. All Markdown applications support these elements.

## Headings

# H1
## H2
### H3
#### H4
##### H5

## Ordered List

1. First item
2. Second item
3. Third item

## Unordered List

- First item
- Second item
- Third item

## Code

`code`

## Horizontal Rule

---

## Link

[Homepage](index.md)

## Image

![coder cat](img/codercat.png)

## Table

| Syntax | Description |
| ----------- | ----------- |
| Header | Title |
| Paragraph | Text |

## Fenced Code Block

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```

## Blockquote

> Rumors of my death have been greatly exaggerated.

## Alerts

> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.

## Formatting

* **Bold text**
* *Italic text*
* ~~Strikethrough~~
* <ins>Underlined</ins>
* e <sup>i π</sup> = -1
* H<sub>2</sub>O

## Footnotes

Here's a sentence with a footnote. [^1]

[^1]: This is the footnote.

## Emoji

`@octocat :+1: This PR looks great - it's ready to merge! :shipit:`

@octocat :+1: This PR looks great :heart: - it's ready to merge! :shipit:

### Task List

- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media
