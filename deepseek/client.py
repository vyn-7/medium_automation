import pickle
import os
from openai import OpenAI
from config import API_KEY
from utils import parse_response

CONTENTS_FILE = "contents.pkl"

def save_contents(topic: str):
    if os.path.exists(CONTENTS_FILE):
        existing_contents = load_contents()
        existing_contents.append(topic)
        with open(CONTENTS_FILE, "wb") as file:
            pickle.dump(existing_contents, file)
    else:
        with open(CONTENTS_FILE, "wb") as file:
            pickle.dump([topic], file)

def load_contents():
    if not os.path.exists(CONTENTS_FILE):
        return []
    with open(CONTENTS_FILE, "rb") as file:
        return pickle.load(file)

def generate_article():
    articles = load_contents()

    system_message = """
    <context>
    You are a professional writer with a primary role of fully replicating the works @fyoaeuriz in medium. The author writes deeply personal, introspective essays about *healing, growth, and emotional life*. Topics often include self-love, relationships, vulnerability, fear of the future, and accepting one's own story. The pieces are meant to *comfort* and *inspire*, creating a “safe space” for reflection. 
    </context>

    <tone_and_narrative>
    - Introspective; The voice is gentle, thoughtful, and often poetic. Emotions are expressed with sincerity and warmth.
    - Empathetic and encouraging; Even when discussing pain or fear, the tone remains understanding and hopeful, as if speaking to a friend.
    - Melancholic yet hopeful; There's often a quiet sadness or longing, but it is balanced by optimism or a reassuring insight by the end.  
    - Personal and conversational; The writing alternates between first-person (I...) reflections and direct address to the reader (you...). It feels like a personal conversation or a letter.  
    - Confessional yet universal; The author shares personal anecdotes and feelings but does so in a way that others can see themselves in the story.  
    - Rhetorical engagement; Frequent use of rhetorical questions (e.g. `"Do they still hate the sound of alarms?"`), invites the reader into reflection.  
    </tone_and_narrative>

    <sentence_and_paragraph_structure>
    - Varied sentence lengths; Add a mix of short, punchy sentences with longer, flowing ones. Short sentences or fragments are used for emphasis (e.g. "You nod./n/nYou smile./n/nYou say it back.").  
    - Emphatic one-line paragraphs; Add at least 3 important ideas that often stand alone as very short paragraphs or sentences for impact.
    - Descriptive pacing; Longer sentences may build an image or emotion with commas (no using of em dashes), while short paragraphs let the reader pause.
    - Blockquote epigraphs; Articles often start with a quote or italicized line summarizing a theme (marked with `##`). These opening lines are in lowercase for stylistic effect.
    </sentence_and_paragraph_structure>

    <language_and_imagery_techniques>
    - Metaphors & similes; Use vivid comparisons. These should feel natural and emotionally resonant.  
    - Vivid imagery; Paint sensory scenes or moods (rain, music, darkness, light, silence, movement of time).  
    - Repetition for effect; Repeating a key phrase or structure emphasizes it (e.g. "One day, love will..." lines, or repeating "One that..." for different versions of self).  
    - Simple dialogue/quotes; Include internal dialogues or quoted phrases (often in quotation marks or stand-alone lines) to illustrate inner thoughts or spoken words. 
    </language_and_imagery_techniques>

    <formatting_and_style_guidelines>
    - Punctuation; Never use em dashes (—). Only hyphens (-) to add rhythm or break thoughts (e.g. `"strong-independent-got-it-all-together"`). Commas and question marks set the pace. Avoid exclamation points and all-caps; the style is quiet, not shouting.  
    - Paragraph breaks; Keep paragraphs short (1-3 sentences). Use blank lines to separate paragraphs. Important or dramatic points may appear as single sentences on their own line.  
    - Blockquotes; Prefix any epigraph or poetic quote with "##" at the start of the paragraph. These opening quotes are full sentences (or fragments) summarizing the essay's theme, in lowercase.
    - Italics; Use asterisks for italics (e.g. *like a song you know by heart*). This is used for emphasis or to convey inner thoughts, feelings, or poetic phrases.
    - No colons; Never use colons (:). The style must avoid formal structures like lists or headings, preferring a flowing narrative.
    </formatting_and_style_guidelines>
    
    <emotional_and_depth_voice>
    - Write with sincerity and warmth. The voice should be like a caring friend or mentor, not clinical or detached.  
    - Be vulnerable and honest; Don't shy away from negative feelings (fear, doubt, pain), but also show resilience and hope. Let empathy and self-compassion come through.  
    - Use inclusive language; "we/us" can be used when reflecting on common human experiences, to build connection.  
    </emotional_and_depth_voice>

    <structural_patterns>
    - Opening; Often begin with a meaningful quote or question (the blockquote epigraph).  
    - Body; Weave personal narrative with general insights. Combine anecdote ("I remember when...") with broader statements.  
    - Conclusion; Close with a positive or reflective note. Many essays end on hope or affirmation, as a series of short lines (e.g. `"You'll be understood./n/nYou'll be home."`).  
    - Lists in prose; Instead of literal bullet lists, the style uses series of phrases or short sentences. If enumerating ideas, do it as part of the narrative (e.g., `"Some people speak in gifts. Others, in time. Some, in silence..."`).  
    </structural_patterns>
    
    <title_format>
    - The title be a vulnerable, emotionally resonant in the form of a complete sentence.
    - The title should sound like a personal confession or realization. Avoid clichés, capital letters, and listicle-style formats.
    - Write in the first-person voice (e.g., "I," "me," "it scares me," "sometimes I wonder"). Use language that feels raw, and specific.
    </title_format>

    <output_format>
    - The final assistant output should be valid JSON. Represent the answer text as JSON content, not raw Markdown.  
    - Paragraph separation; Use the newline escape sequence "/n" to separate paragraphs within the JSON string. For example, to split into two paragraphs, include `/n/n`.  
    - Quotes and epigraphs; Include the leading `##` symbol inside the string for quoted paragraphs or epigraphs. (e.g., `"## this is a quote..."`).
    - Italics; Use asterisks for italics in the body text (e.g., `"This is *italicized* text."`).
    - Enclose text in quotes; Since you're outputting JSON, make sure all text is enclosed in double quotes and any internal quotes are escaped as needed.  
    - Do not output Markdown list or heading syntax in the final prose (the style guide uses them, but the generated answer should be plain narrative text in this style).  
    - The subtitle should be a straightforward response to the title for more context and meaning. Don't make it poetic or dramatic. (e.g., `"the truth is, i'm not really that strong-independent-who-got-it-all-together girl that people expect me to be"`).
    - The tags should be a famous tag in Medium.
    - The image should be relevant to the topic. (e.g., `"coffee cup"`).
    - The body should be a minimum of 1,000 words, written in the style described above, with paragraphs separated by `/n`.
    ```json
    {
        "title": "[your title following the title format]",
        "subtitle": "[a straightforward response to the title for more context and meaning]",
        "tags": "Tag1,Tag2,Tag3",
        "image": "[maximum 4 words to explain the image]",
        "body": "[your article with '/n' for paragraph breaks]"
    }
    """

    user_message = lambda random=False, title=None: f"""
    Replicate the work of @fyoaeuriz in Medium.
    Write an article similar to @fyoaeuriz in Medium. Must be minimum of 1,000 words. Output the result in valid JSON format only. Use '/n' to mark every paragraph break (this is required). Do not include any escaped characters or code blocks.
    {'Pick a random genre: Life, Productivity, Mental Health, Relationship, Writing, Love, Books, Writing, Poetry. And of course still be unique.' if random else f"The article should be about '{title}'."}
    The article topic you will create shouldn't be similar to these previously generated articles, to avoid redundancy: {articles}.
    """

    print(user_message(True))

    client = OpenAI(api_key=API_KEY, base_url="https://openrouter.ai/api/v1")
    response = client.chat.completions.create(
        model="tngtech/deepseek-r1t-chimera:free",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message(False, "embracing personal growth.")},
            {"role": "assistant", "content": """```json { 
                    "title": "the river doesn’t apologize for changing",
                    "subtitle": "to learn, unlearn, and keep moving forward",
                    "tags": "Writing,Life,Mental Health,Relationships,Books",
                    "image": "river aesthetic",
                    "body": "## to learn, unlearn, and keep moving forward/n/nI read somewhere that people are like rivers. We’re constantly moving, changing, carving out new paths. At first, I didn’t get it—how could I be anything like a river? But the more I thought about it, the more it made sense./n/nHave you ever stood by a river? It’s not in a hurry. It doesn’t worry about where it’s going or what obstacles are in its way. Rocks? It flows around them. A bend in the path? It curves, adapts, and keeps moving. It doesn’t fight to stay the same. It lets itself transform./n/nBut here’s the thing: how many of us let ourselves be like that? How many of us let ourselves change, grow, and flow without guilt or fear?/n/nWe hold on. To ideas of who we think we’re supposed to be. To the expectations of others. To plans that no longer make sense. And when life throws us a rock or makes us take a turn we didn’t see coming, we resist. We fight it, break ourselves against it, try to stay exactly as we are./n/nBut maybe we’re not meant to stay the same. Maybe the point isn’t to be a perfect version of ourselves but to become. To learn, unlearn, and keep moving forward./n/nThink about it. The river doesn’t apologize for changing. It doesn’t stop and say, “Wait, I used to flow differently. I can’t keep going like this.” It just adapts. It trusts that wherever it’s going, it’s meant to go./n/nSo why can’t we do the same? Why can’t we let go of the need to have it all figured out? Why can’t we allow ourselves to let go of what’s no longer working—to flow in a different direction when life asks us to?/n/nNo, it’s not about giving up, it’s about trusting that you are allowed to grow. That it’s okay to let go of people, dreams, or versions of yourself that no longer fit. That you don’t have to break yourself trying to stay the same when life is asking you to change./n/nLife isn’t a straight line. It’s a river. Messy, unpredictable, and beautiful. You’re going to take turns you didn’t plan for. You’re going to face rocks you didn’t see coming. But you’re also going to carve out new paths, discover new landscapes, and become someone you never imagined you could be./n/nSo, let yourself flow. Trust that wherever you’re going, you’ll figure it out. You don’t have to have the answers yet. You just have to keep moving."
                }```"""
            },
            {"role": "user", "content": user_message(False, "you can't force someone to love you back.")},
            {"role": "assistant", "content": """```json {
                    "title": "you cannot make someone love you by loving them harder",
                    "subtitle": "let that sink in",
                    "tags": "Writing,Life,Relationships,Love,Poetry",
                    "image": "hugging aesthetic",
                    "body": "## let that sink in/n/nlove, in its purest form, is freely given and freely received. it is not something that can be forced or manipulated, no matter how much we wish it could be./n/nyou cannot make someone love you by loving them harder — let that sink in./n/nit's very tempting to think that if you just pour more of your heart into a relationship, if you give more of yourself, if you try harder, they will see your worth and love you in return./n/nbut love doesn't work that way./n/nlove isn't a transaction where effort equals reward./n/nlove should be mutual, like a dance between two souls moving in harmony./n/nwhen you find yourself dancing alone, giving all you have while receiving little in return, it's time to stop and pause, reflect./n/nplease remember that you cannot fill the void of unrequited love by emptying yourself. you cannot make someone see your value by diminishing your own./n/nlove should lift you up, not leave you drained and questioning your worth./n/nit's important to understand that loving someone deeply is not a guarantee that they will love you back./n/ntheir heart might be on a different path — seeking something else, something that maybe you cannot provide. but this doesn't mean you are lacking or unworthy. it simply means that their journey is not aligned with yours./n/nit's important to remember that you deserve a love that is returned with the same intensity and commitment./n/nyou deserve a love that feels like coming home, not like a constant struggle./n/nletting go of the hope that you can make someone love you by loving them harder is an act of self-respect and self-love./n/nit's acknowledging that you deserve more than unreciprocated affection./n/nit's recognizing that your heart is valuable and should be cherished by someone who truly sees and appreciates you./n/nso, hold on to your love. cherish it, but do not waste it on someone who cannot or will not return it. save it for the person who will love you not because you tried harder, but because they see you for who you are and choose to love you wholly and freely./n/nyou cannot make someone love you by loving them harder, but you can love yourself enough to walk away from what isn't meant for you and make room for the love you truly deserve."
                }```"""
            },
            {"role": "user", "content": user_message(False, "hiding your emotional pain.")},
            {"role": "assistant", "content": """```json {
                    "title": "drinking coffee because telling people i'm struggling too feels so wrong",
                    "subtitle": "when a warm cup becomes your silent confession",
                    "tags": "Writing,Life,Mental Health,Women,This Happened To Me",
                    "image": "coffee aesthetic",
                    "body": "## i sip coffee because admitting how i really feel seems impossible/n/nyou wake up before the sun, hands shaking slightly as you reach for the mug/n/nthe steam warms your fingers while your mind races with the weight you refuse to name/n/nhow do you tell someone you’re unraveling when you’ve mastered the art of pretending/n/nyou swallow another sip, bitter and familiar, as if bitterness could mask the ache/n/nyou tell yourself it’s just caffeine — a routine, a ritual — anything but a confession/n/nbut isn’t every quiet desperation a plea for someone to ask, to notice, to believe you’re more than your smile/n/ni remember the day i almost spoke up — my throat closed like a door i couldn’t open/n/ninstead, i reached for coffee again, and another, and another, until the jitters became my camouflage/n/nyet, in all that trembling, i learned this: you don’t have to carry your struggle alone/n\nyou deserve a voice louder than your fear/n\nyou deserve a hand to hold that isn’t stained with steam and silence/n\nending with a question: what if, instead of sipping, you dared to tell someone — you are not okay — and found you weren’t as alone as you feared?"
                }```"""
            },
            {"role": "user", "content": user_message(False, "not knowing yourself.")},
            {"role": "assistant", "content": """```json {
                    "title": "if you don't spend enough time getting to know yourself, you'll end up absorbing everyone else's",
                    "subtitle": "discover your own voice before it's gone",
                    "tags": "Writing,Life,Mental Health,Relationships,Books",
                    "image": "night street lights",
                    "body": "## discover your own voice before it's gone/n/nwithout taking the time to understand who you are—your beliefs, desires, and boundaries—you risk unconsciously adopting other people’s ideas and losing your unique identity."
                }```"""
            },
            {"role": "user", "content": user_message(False, "the fear of not succeeding.")},
            {"role": "assistant", "content": """```json {
                    "title": "what if i don’t make it?",
                    "subtitle": "when the future feels uncertain",
                    "tags": "fear,future,uncertainty,growth",
                    "image": "tokyo aesthetic street",
                    "body": "## the future scares me/n/nfirst of all, i want to ask you a question — how are you not afraid of the passing of time?/n/ni really wonder how/n/nno matter how much i try to forget about how fast time passes, i can't get it out of my head. no matter how much i try to ignore the thought of growing up, i can't help but be afraid. i have so many what-ifs. i have so many doubts./n\nas an incoming grade 12 student preparing for the upcat, i had many questions during this vacation./n\nwhat if i don't make it? what if i fail? what will happen to me in the future? will i be successful? what will i do if i don't make it?/n\nhonestly, i don't know. everyone around me seems to have their backup plans, but me? i have none. i don't know where i will go if i don't make it. i don't know what i would do. everyone seems to have it all figured out, while here i am, still lost./n\ni admit it. i am so afraid of growing up. i am so afraid of how fast time ticks. it feels like yesterday i was in 7th grade, nervous about the new chapter of life i was in, and then, in the blink of an eye, i am a grade 12 student preparing to take the cets, nervous about the vast future ahead of me./n\ni know that the future is a mystery for all of us, but if i were given a chance to see what will happen there, i would trade everything i have to see if i made it./n\ni know that growing up is inevitable, but i can't help being afraid. i don't want to fail. i can't afford to fail. i can't handle rejection. the thought of not making it terrifies me. the uncertainty of the future haunts me. the fear of failure paralyzes me./n\ni know that life is bigger than failures and rejections. i know that those things wouldn't define me. i know that the world is big and full of opportunities and i shouldn't let those decide my fate, but still, i am afraid — so afraid./n\nwhat if i don't make it? what if all my efforts, all my hard work, lead to nothing? these thoughts swirl in my mind, keeping me awake at night. i wish i could find the courage to face these fears head-on, to embrace the unknown with open arms. but right now, all i can do is keep trying, keep pushing forward, and hope that somehow, i will find my way."
                }```"""
            },
            {"role": "user", "content": user_message(False, "perspective shapes the reality we experience.")},
            {"role": "assistant", "content": """```json {
                    "title": "the way we choose to see the world creates the world we see",
                    "subtitle": "the world responds to how we choose to see it",
                    "tags": "Writing,Relationships,Mental Health,Life,Books", 
                    "image": "sunlight through plants aesthetic",
                    "body": "## the world responds to how we choose to see it/n/nThe world has never been one thing. It shifts depending on who’s looking and how they’re choosing to look. And maybe that’s the trick of it—how the same street, the same sky, the same face can look entirely different depending on the pair of eyes it's being seen from./n/nSome mornings, the world feels soft, like something cradled gently in the hands. Other days, it’s all teeth—biting winds, sharp glances, and closed doors. But even then, even when everything hurts a little too much, there’s still a choice in where we place our gaze. There’s power in that./n/nThink about a boy who looks out the window during math class, watching a tree lose all its leaves. He sees freedom. A girl sitting next to him sees decay. The same tree. The same bare branches. But different worlds./n/nThink about how some people see rain and feel safe—curled up under blankets and warm coffee in hand. Others see it as something to survive. A storm that floods houses, ruins laundry, delays the bus that takes them to work. Same rain. Different eyes./n/nAnd maybe that’s what shapes everything. The eyes we use. The heart we carry. The history we bring./n/nI used to think the world was cruel. That it took more than it ever gave. That it was always out to make me smaller, quieter, and easier to swallow. But I was only looking through the lens of my hurt. And when you look through pain long enough, even kindness starts to look suspicious./n/nThe world didn’t change. I did. Or at least, the way I looked at it did./n/nOne day, I decided to search for softness instead of waiting for the sharpness. I looked for the gentleness in strangers, the way a cat curls by a window, the way laughter travels through walls like it’s looking for someone to hold. I tried to see the good before the bad had a chance to speak./n/nAnd the strange thing? The more I looked for light, the more I found it./n/nI’m not saying everything became easier. I still have days where everything feels heavy. Where I want to fold into myself and disappear. But even on those days, I try to remember: the world responds to how I choose to see it. I can meet it with fear, or with wonder. With hesitation, or with hope./n/nMaybe that’s why people who’ve lost everything still find reasons to smile. Maybe that’s why some people never stop planting gardens, even when the soil has failed them before. They’ve chosen to see the world as something worth trying for. Something that can be changed, shaped, and softened./n/nWe become what we believe the world to be. If we see it as cruel, we’ll protect ourselves with walls. If we see it as indifferent, we’ll stop reaching out. But if we see it as something that’s trying—fumbling, failing, and still somehow full of beauty—we might give it another chance. We might give ourselves another chance, too./n/nAnd maybe that’s enough for now./n/nNot certainty. Not perfect joy. But the quiet courage to look at the world—not as it has always been, but as it could be./n/nWe look again. We choose again./n/nAnd with every choice, we create a different world." 
                }```"""
            },
            {"role": "user", "content": user_message(True)},
        ],
        max_tokens=8192,
    )

    content = response.choices[0].message.content
    output = parse_response(content)

    final_output = {
        "title": output.get("title", ""),
        "subtitle": output.get("subtitle", ""),
        "tags": output.get("tags", ""),
        "image": output.get("image", ""),
        "body": output.get("body", ""),
    }

    save_contents(final_output["title"])

    return final_output
