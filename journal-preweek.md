** Preweek 0 **

# Language learning thoughts/notes - 'vocab' drills

## Underpinning recall for e.g. vocab and in-context (sentence) learning = scheduling reviews optimally
- overview of the concepts of SRS - https://juliensobczak.com/inspect/2022/05/30/anki-srs/ - with 
- history: early concepts of the 'forgetting curve' Hermann Ebbinghaus (1885) through 'spacing' Skinner to boost recall in the 50s with Sebastian Leitner (1972) implementing initially as card index by manually moving physical cards between review frequency buckets!
- discussion of algorithms, what is used in various systems and services, further links/history plus code snippets
- :thought_balloon: retention/review generally fixed - could ML enable tuning at learner level _e.g._ periods of review changes by user; period of review schedulings changes by performance on that specific item; review frequency changes by 'class' or 'type' item being learnt

## Open source tooling
- Anki https://apps.ankiweb.net/ - spaced repetition system (SRS) - multiplatform with web-based sync service
- https://github.com/yomidevs/yomitan (including capture from web, audio TTS, kanji stroke order - all from linked services/data sources)
- _c.f._ &#24460; sentence parsing/decomposition e.g. https://taku910.github.io/mecab/#diff
- :thought_balloon: can we/how might we enrich GenAI usefulness by augmenting with these services and underlying data sources, either in training/tuning models upfront, RAG, vs 'enriching' the model's output with services or additional static or dynamic data 

## Commercial
- as well as the 'big player' multi-language offerings there are some specific to Japanese which have grown up more organically from the ground-up e.g. mnemonic-based kanji and vocab in https://www.wanikani.com/


# Real learning supported by LLMs or on-demand subsitution for understanding
- gulf between asking an LLM to summarise a topic/write some code and an understanding of a topic or getting to 'good' 
- some of the chatter on our Discord and my own reading this week -> if you understand something already then GenAI can act as a force multiplier, and where you don't can enable progress and basic progress in a fake it till you make it mode which isn't a bad thing but isn't a panacea. 
- prevalent in many blog posts I've been reading this week especially on LinkedIn = pick a hot topic and press create... doesn't give an interesting/balanced/informed take on things :(
- Andrew and Quincy discussed similar 'meta' in fireside chat


# The woes of purchasing local hardware - notes

## hardware to inference 'good' models (parameter size/quantization) at 'reasonable' performance still hard to source especially for homelab-type used
- smaller models can be run, but larger more challenging and tuning etc. remains out of reach (understandably)
- at a personal level from YouTube and blog investigations...
- reasonable speed broadly considered 20+ tokens per second for LLM conversational use, although power-users think 40+
- M4 macs an option and MLX performance specifically tuned over GGUF format but RAM subject to Apple tax on memory upgrades
- nVidia still dominates with implementation and hardware but 50-series again in effect a paper launch
  - 5090 Founders at £2k even if you could source (scalpers) and partner cards ++; coverage on 5080 mixed at best, 5070Ti will have 16Gb like 5080 so might be cost-effective fast-enough option... but launch end Jan-25 and expected 4 months+ before stock actually available in retail channels at/near RRP in UK
  - Jetson Orin nano small form factor received recent boost (to 'Super') but no change to hardward - uplift all from software - maxes out at 8Gb and although RRP circa £250 GBP - board and carrier without case etc. - backordered
  - DIGITS announced at £3k GBP for serious players - two can be NVlinked and model layers shared = much faster interconnect bandwidth... NVLink > Thunderbolt > ethernet > wifi

## lots of good content here on Youtube
- notably https://www.youtube.com/@AZisk/videos re: hands-on performance of LLMs locally - nVidia GPUs, Macs, a Mac cluster(!) etc.
- good for getting a sense of real-world LLM performance as runs through permutations of hardware, models, quants and limitations in 'clusters' (exo etc.)
