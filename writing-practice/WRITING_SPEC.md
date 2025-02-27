# Writing Practice

## Business Goal: 
Students have asked if there could be a learning exercise to practice writing words.

You have been tasked to build a prototyping application which will take a word group, and generate very simple sentences in english, and you must write them in Japanese.


Technical Requirements:
- Streamlit
- MangaOCR (Japanese)
- Be able to upload an image

## Technical spec

### Launch from lang-portal
- launch via new activity: "Practice handwriting words"
-- store public exposed endpoint of running Lightning studio in Activities table



## Implementation approach

Darya Petrashka
https://github.com/dashapetr/kana--streamlit-app

[X] Rehost Darya's Streamlit app using Lightning AI
[] sleep

- using a specific word group generate a list of sentences in Japanese
-- at a specified JLPT level e.g. N5, N4 etc.
-- use a random word from the group in each sentence
-- output the sentence in Japanese with that word missing e.g. 
-- include the word in the sentence in the output in square brackets after the sentence e.g.  


### LLM input prompt
- you are a Japanese language learning expert.
- generate 10 sentences in Japanese at N5 level using a random word from a supplied list of words.
- use a random word from the input list of words for each sentence
- output the sentence in Japanese with that word missing, returning the result in a JSON object with the following structure:

example output for reference.  always use this structure
{
  "questions": [
    {
      "question": {
        "japanese": "この料理は___ですね。",
        "english": "This food is [delicious], isn't it?"
      },
      "answer": {
        "kanji": "おいしい",
        "kana": "おいしい",
        "romaji": "oishii"
      }
    },
    {
      "question": {
        "japanese": "今日の天気は___です。",
        "english": "Today's weather is [cold]."
      },
      "answer": {
        "kanji": "寒い",
        "kana": "さむい",
        "romaji": "samui"
      }
    },
    {
      "question": {
        "japanese": "私の弟は___です。",
        "english": "My little brother is [kind]."
      },
      "answer": {
        "kanji": "優しい",
        "kana": "やさしい",
        "romaji": "yasashii"
      }
    },
    {
      "question": {
        "japanese": "彼女の声は___です。",
        "english": "Her voice is [quiet]."
      },
      "answer": {
        "kanji": "静か",
        "kana": "しずか",
        "romaji": "shizuka"
      }
    },
    {
      "question": {
        "japanese": "このかばんは___です。",
        "english": "This bag is [heavy]."
      },
      "answer": {
        "kanji": "重い",
        "kana": "おもい",
        "romaji": "omoi"
      }
    },
    {
      "question": {
        "japanese": "新しい車は___ですか？",
        "english": "Is the new car [expensive]?"
      },
      "answer": {
        "kanji": "高い",
        "kana": "たかい",
        "romaji": "takai"
      }
    },
    {
      "question": {
        "japanese": "この映画は___ですね。",
        "english": "This movie is [interesting], isn't it?"
      },
      "answer": {
        "kanji": "面白い",
        "kana": "おもしろい",
        "romaji": "omoshiroi"
      }
    },
    {
      "question": {
        "japanese": "あの建物は___です。",
        "english": "That building is [old]."
      },
      "answer": {
        "kanji": "古い",
        "kana": "ふるい",
        "romaji": "furui"
      }
    },
    {
      "question": {
        "japanese": "私の部屋は___です。",
        "english": "My room is [narrow]."
      },
      "answer": {
        "kanji": "狭い",
        "kana": "せまい",
        "romaji": "semai"
      }
    },
    {
      "question": {
        "japanese": "私の家は___です。",
        "english": "My house is [pretty]."
      },
      "answer": {
        "kanji": "綺麗",
        "kana": "きれい",
        "romaji": "kirei"
      }
    }
  ]
}

Input word list 

  {
    "kanji": "近い",
    "romaji": "chikai",
    "english": "near; close",
    "parts": [
      { "kanji": "近", "romaji": ["chi","ka"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
  {
    "kanji": "詰らない",
    "romaji": "tsumaranai",
    "english": "boring",
    "parts": [
      { "kanji": "詰", "romaji": ["tsu","ma"] },
      { "kanji": "ら", "romaji": ["ra"] },
      { "kanji": "な", "romaji": ["na"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
  {
    "kanji": "遠い",
    "romaji": "tooi",
    "english": "far",
    "parts": [
      { "kanji": "遠", "romaji": ["to","o"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
  {
    "kanji": "有名",
    "romaji": "yuumei",
    "english": "famous",
    "parts": [
      { "kanji": "有", "romaji": ["yu","u"] },
      { "kanji": "名", "romaji": ["me","i"] }
    ]
  },
  {
    "kanji": "長い",
    "romaji": "nagai",
    "english": "long",
    "parts": [
      { "kanji": "長", "romaji": ["na","ga"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },



input words
  {
    "kanji": "近い",
    "romaji": "chikai",
    "english": "near; close",
    "parts": [
      { "kanji": "近", "romaji": ["chi","ka"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
  {
    "kanji": "詰らない",
    "romaji": "tsumaranai",
    "english": "boring",
    "parts": [
      { "kanji": "詰", "romaji": ["tsu","ma"] },
      { "kanji": "ら", "romaji": ["ra"] },
      { "kanji": "な", "romaji": ["na"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
  {
    "kanji": "遠い",
    "romaji": "tooi",
    "english": "far",
    "parts": [
      { "kanji": "遠", "romaji": ["to","o"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
  {
    "kanji": "有名",
    "romaji": "yuumei",
    "english": "famous",
    "parts": [
      { "kanji": "有", "romaji": ["yu","u"] },
      { "kanji": "名", "romaji": ["me","i"] }
    ]
  },
  {
    "kanji": "長い",
    "romaji": "nagai",
    "english": "long",
    "parts": [
      { "kanji": "長", "romaji": ["na","ga"] },
      { "kanji": "い", "romaji": ["i"] }
    ]
  },
 {
    "kanji": "買い物する",
    "romaji": "kaimonosuru",
    "english": "to shop",
    "parts": [
      { "kanji": "買", "romaji": ["ka"] },
      { "kanji": "い", "romaji": ["i"] },
      { "kanji": "物", "romaji": ["mo", "no"] },
      { "kanji": "す", "romaji": ["su"] },
      { "kanji": "る", "romaji": ["ru"] }
    ]
  },
  {
    "kanji": "帰る",
    "romaji": "kaeru",
    "english": "to return",
    "parts": [
      { "kanji": "帰", "romaji": ["ka", "e"] },
      { "kanji": "る", "romaji": ["ru"] }
    ]
  },
  {
    "kanji": "書く",
    "romaji": "kaku",
    "english": "to write",
    "parts": [
      { "kanji": "書", "romaji": ["ka"] },
      { "kanji": "く", "romaji": ["ku"] }
    ]
  },
  {
    "kanji": "観光する",
    "romaji": "kankousuru",
    "english": "to sightsee",
    "parts": [
      { "kanji": "観", "romaji": ["kan"] },
      { "kanji": "光", "romaji": ["kou"] },
      { "kanji": "す", "romaji": ["su"] },
      { "kanji": "る", "romaji": ["ru"] }
    ]
  },
  {
    "kanji": "聞く",
    "romaji": "kiku",
    "english": "to listen",
    "parts": [
      { "kanji": "聞", "romaji": ["ki"] },
      { "kanji": "く", "romaji": ["ku"] }
    ]
  },
  {
    "kanji": "来る",
    "romaji": "kuru",
    "english": "to come",
    "parts": [
      { "kanji": "来", "romaji": ["ku"] },
      { "kanji": "る", "romaji": ["ru"] }
    ]
  },
  {
    "kanji": "する",
    "romaji": "suru",
    "english": "to do",
    "parts": [
      { "kanji": "す", "romaji": ["su"] },
      { "kanji": "る", "romaji": ["ru"] }
    ]
  },
  {
    "kanji": "食べる",
    "romaji": "taberu",
    "english": "to eat",
    "parts": [
      { "kanji": "食", "romaji": ["ta"] },
      { "kanji": "べ", "romaji": ["be"] },
      { "kanji": "る", "romaji": ["ru"] }
    ]
  },