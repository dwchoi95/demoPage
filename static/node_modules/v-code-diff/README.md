# VCodeDiff

[![NPM version](https://img.shields.io/npm/v/v-code-diff.svg?style=flat)](https://www.npmjs.com/package/v-code-diff) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/npm/dt/v-code-diff?minimal=true)](https://www.npmjs.com/package/v-code-diff)

A code diff display plugin, available for Vue2 / Vue3. It is the vue3 version
of [vue-code-diff](https://github.com/ddchef/vue-code-diff), refer to a lot of code, thanks here.

> [🇨🇳 中文文档](./README-zh.md)

# Installation

Install `v-code-diff`

```shell
# With NPM
npm i v-code-diff

# With Yarn
yarn add v-code-diff
```

Vue2 developers need install composition-api

```shell
yarn add @vue/composition-api
```

# Getting started

### `Vue3`

#### Register globally

```ts
import {createApp} from 'vue'
import CodeDiff from 'v-code-diff'

app
    .use(CodeDiff)
    .mount('#app')
```

Then

```vue

<template>
  <code-diff
      :old-string="'12345'"
      :new-string="'3456'"
      file-name="test.txt"
      output-format="side-by-side"/>
</template>
```

#### Register locally

in vue file

```vue

<template>
  <code-diff
      :old-string="'12345'"
      :new-string="'3456'"
      file-name="test.txt"
      output-format="side-by-side"/>
</template>
<script lang="ts">
import {defineComponent} from 'vue'
import {CodeDiff} from 'v-code-diff'

export default defineComponent({
  components: {
    CodeDiff
  }
})
</script>

```

### `Vue2`

#### Register globally

```ts
import Vue from 'vue';
import CodeDiff from 'v-code-diff'

Vue.use(CodeDiff);
```

#### Register locally

```vue

<template>
  <code-diff
      :old-string="'12345'"
      :new-string="'3456'"
      file-name="test.txt"
      output-format="side-by-side"/>
</template>
<script>
import {CodeDiff} from 'v-code-diff'

export default {
  name: 'App',
  components: {
    CodeDiff
  }
}
</script>
```

# Events

| Event Name   | Description    | Callback Params   |
|---------- |-------- |---------- |
| before-render | hook before rendering | -  |
| after-render | hook after rendering | -  |

# Props

| Prop      | Description    | Type      | Optional       | Default   |
|---------- |-------- |---------- |-------------  |-------- |
| highlight| control whether to highlight the code | boolean  |   -    |    true     |
| language| code language，such as `typescript`. If you don't input, it will be judged automatically. [view all supported languages](https://github.com/highlightjs/highlight.js/blob/main/SUPPORTED_LANGUAGES.md)  | string  |   -    |   -     |
| old-string| old string | string  |   -    |    -     |
| new-string| new string| string  |   -    |    -     |
| context| number of show context lines | number  |   -    |    -     |
| outputFormat| show method | string  |   line-by-line，side-by-side    |    line-by-line     |
| drawFileList | show files list | boolean | - | false |
| renderNothingWhenEmpty | render nothing when empty | boolean | - | false |
| diffStyle | difference style | string | word, char | word |
| fileName | file name | string | - |  |
| isShowNoChange | show raw when no change | boolean | - | false |
| trim | Remove blank characters before and after the string | boolean | - | false |
| language | code language | boolean | - | false |
| noDiffLineFeed | Do not diff windows line feed (CRLF) and linux line feed (LF)  | boolean | - | false |

# Difference from [vue-code-diff](https://github.com/ddchef/vue-code-diff)

* Support `vue3`
* Smaller package size
* Faster rendering speed

# ChangeLog

### 0.3.8

1. Style adjustment, hide css `d2h-file-header`, same as vue-code-diff
2. Add prop `noDiffLineFeed`, do not diff windows line feed (CRLF) and linux line feed (LF)

### 0.3.7

1. Fix the problem of displaying "File Without Change..." when isShowNoChange is true and the old and new codes are different,
then show all the source code

### 0.3.6

1. Add prop `language`, make highlighting more accurate

### 0.3.5

1. In the side-by-side mode, support left and right synchronous scrolling

### 0.3.4

1. Add Prop `trim`, it will remove the blank characters before and after the string

### 0.3.3

1. Fixed the problem of highlight failure.

### 0.3.2

1. Fixed the warning for vue2 users in console

### 0.3.1

1. Fix incorrect style when comparing text

### 0.3.0

1. Performance optimization, now rendering has better performance
2. Add Prop `diffStyle` to control whether to display word-level differences or char-level differences

### 0.2.1

1. Use the function of asynchronous rendering of the highlight code, without blocking the ui, greatly improving the page
   rendering speed
2. Add hook function (before rendering, after rendering): `before-render`, `after-render`

### 0.1.0

1. Add prop `highlight` to control whether to highlight the code.

### 0.0.4

1. Fix the problem of abnormal rendering in some browsers (such as safari)

### 0.0.3

1. Prop: `context` default value changed from 5 to 10
2. fix possible line-height conflict(such as `antd.css` in [antd-vue](https://github.com/vueComponent/ant-design-vue))

### 0.0.1

First Version.

# LICENCE

MIT License

Copyright (c) 2021 Shimada666

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
