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
    {'Pick a random genre: Life, Future, This Happened To Me, Growing Up, Productivity, Mental Health, Relationship, Writing, Love, Books, Writing, Poetry. And of course still be unique.' if random else f"The article should be about '{title}'."}
    The article topic you will create shouldn't be similar to these previously generated articles, to avoid redundancy: {articles}.
    """

    print(user_message(True))

    client = OpenAI(api_key=API_KEY, base_url="https://openrouter.ai/api/v1")
    response = client.chat.completions.create(
        model="tngtech/deepseek-r1t-chimera:free",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message(False, "you can't force someone to love you back.")},
            {"role": "assistant", "content": """```json {
                    "title": "you cannot make someone love you by loving them harder",
                    "subtitle": "let that sink in",
                    "tags": "Writing,Life,Relationships,Love,Poetry",
                    "image": "hugging aesthetic",
                    "body": "## let that sink in/n/nLove, in its purest form, is freely given and freely received. It is not something that can be forced or manipulated, no matter how much we wish it could be./n/nYou cannot make someone love you by loving them harder—let that sink in./n/nIt’s very tempting to think that if you just pour more of your heart into a relationship, if you give more of yourself, if you try harder, they will see your worth and love you in return./n/nBut love doesn’t work that way./n/nLove isn’t a transaction where effort equals reward./n/nLove should be mutual, like a dance between two souls moving in harmony./n/nWhen you find yourself dancing alone, giving all you have while receiving little in return, it’s time to stop and pause, reflect./n/nPlease remember that you cannot fill the void of unrequited love by emptying yourself. You cannot make someone see your value by diminishing your own.\n\nLove should lift you up, not leave you drained and questioning your worth.\n\nIt’s important to understand that loving someone deeply is not a guarantee that they will love you back.\n\nTheir heart might be on a different path — seeking something else, something that maybe you cannot provide. But this doesn’t mean you are lacking or unworthy. It simply means that their journey is not aligned with yours.\n\nIt’s important to remember that you deserve a love that is returned with the same intensity and commitment.\n\nYou deserve a love that feels like coming home, not like a constant struggle.\n\nLetting go of the hope that you can make someone love you by loving them harder is an act of self-respect and self-love.\n\nIt’s acknowledging that you deserve more than unreciprocated affection.\n\nIt’s recognizing that your heart is valuable and should be cherished by someone who truly sees and appreciates you.\n\nSo, hold on to your love. Cherish it, but do not waste it on someone who cannot or will not return it. Save it for the person who will love you not because you tried harder, but because they see you for who you are and choose to love you wholly and freely./n/nYou cannot make someone love you by loving them harder, but you can love yourself enough to walk away from what isn’t meant for you and make room for the love you truly deserve."
                }```"""
            },
            {"role": "user", "content": user_message(False, "hiding your emotional pain.")},
            {"role": "assistant", "content": """```json {
                    "title": "drinking coffee because telling people i'm struggling too feels so wrong",
                    "subtitle": "the truth is, i’m not really that strong-independent-who-got-it-all-together girl that people expect me to be",
                    "tags": "Writing,Life,Mental Health,Women,This Happened To Me",
                    "image": "coffee aesthetic",
                    "body": "## the truth is, i’m not really that strong-independent-who-got-it-all-together girl that people expect me to be/n/nIn this society where every person I meet seems to have it all together, admitting that I am struggling too feels embarrassing because there's like this unspoken rule that I should always be strong, independent, in control, anything that doesn't show any weakness, any vulnerability./n/nBut then, I know… I know like the back of my hand that most of us are just pretending, masking our struggles away with this facade of smiles and laughter./n/nBecause behind every smile, every laugh, every confident and composed look is another version of me that's too broken, too wounded, imperfect./n/nThe pressure to be perfect seems unbearable, making it hard for me to tell anyone that I’m not okay, that I’m struggling./n/nThat I need their hands to hold me because I am slowly drowning in this wave of hidden emotions./n/nI often feel like if I show people the wounded, broken, and vulnerable parts of me, they will think less of me, and judge me./n/nSo, I bottle it all up, sip on my coffee, and suffer in silence because that's how I thought suffering should be — hidden, in silence./n/nBut you wanna know the truth?/n/nHiding our pain doesn't make it go awa
                }```"""
            },
            {"role": "user", "content": user_message(False, "not knowing yourself.")},
            {"role": "assistant", "content": """```json {
                    "title": "if you don’t spend enough time getting to know yourself, you’ll end up absorbing everyone else’s definition of you",
                    "subtitle": "you owe it to yourself to live a life that’s yours",
                    "tags": "Writing,Life,Mental Health,Relationships,Books",
                    "image": "night street lights",
                    "body": "## you owe it to yourself to live a life that’s yours/n/nI saw a video on TikTok the other day, and it said, “If you don’t spend enough time getting to know yourself, you’ll end up absorbing everyone else’s definition of you.” And it hit me—how often do we let that happen? How often do we let the world, our friends, our families, even strangers, tell us who we are?\n\nThink about it.\n\nIf you don’t take the time to figure out what you love, what you stand for, and what makes you come alive, someone else will decide it for you. And the scary part is, you might not even notice it happening. One day you’ll wake up and realize you’ve been living a life shaped by everyone else’s opinions—except your own.\n\nIt doesn’t happen all at once. When someone tells you, “You’re too sensitive,” so you stop expressing your emotions. Or when they say, “You’re so quiet,” so you force yourself to speak even when you don’t want to. Or when they imply you’re not enough as you are, so you spend years trying to be someone else.\n\nAnd for what? To please them? To fit in? To feel worthy?\n\nLet me tell you this: no one else gets to define you. Not your friends, not your parents, not society. Only you can do that. But here’s the thing—it takes work. It takes sitting with yourself, asking hard questions, and being brutally honest about what you want and who you are. It’s not easy. It’s messy, uncomfortable, and sometimes lonely. But it’s worth it.\n\nBecause the alternative? It’s living your life like a mirror, reflecting everyone else’s expectations but never showing your true self. It’s waking up one day and realizing you don’t even know who you are anymore.\n\nSo, I’m asking you, right here and now: When was the last time you spent time getting to know yourself? When was the last time you asked yourself, “What do I really want? What makes me happy? What do I believe in?”\n\nIf you don’t have the answers yet, that’s okay. But start asking. Start paying attention to the things that light you up and the things that drain you. Start saying no to what doesn’t feel right, even if it disappoints others. Start saying yes to the parts of yourself you’ve ignored for too long.\n\nYou owe it to yourself to live a life that’s yours. A life where you know who you are and stand firm in it. Because the world will always try to tell you who to be. But you? You get to decide whether to listen."
                }```"""
            },
            {"role": "user", "content": user_message(False, "the fear of not succeeding.")},
            {"role": "assistant", "content": """```json {
                    "title": "what if i don’t make it?",
                    "subtitle": "the future scares me",
                    "tags": "Writing,Future,Life,Growing Up,This Happened To Me",
                    "image": "tokyo aesthetic street",
                    "body": "## the future scares me/n/nFirst of all, I want to ask you a question—how are you not afraid of the passing of time?/n/nI really wonder how/n/nNo matter how much I try to forget about how fast time passes, I can't get it out of my head. No matter how much I try to ignore the thought of growing up, I can't help but be afraid. I have so many what-ifs. I have so many doubts./n/nAs an incoming grade 12 student preparing for the UPCAT, I had many questions during this vacation./n/nWhat if I don't make it?/n/nWhat if I fail?/n/nWhat will happen to me in the future?/n/nWill I be successful? what will I do if I don't make it?/n/nHonestly, I don't know. Everyone around me seems to have their backup plans, but me? I have none. I don't know where I will go if I don't make it. I don't know what I would do. Everyone seems to have it all figured out, while here I am, still lost./n/nI admit it. I am so afraid of growing up. I am so afraid of how fast time ticks. It feels like yesterday I was in 7th grade, nervous about the new chapter of life I was in, and then, in the blink of an eye, I am a grade 12 student preparing to take the CETs, nervous about the vast future ahead of me./n/nI know that the future is a mystery for all of us, but if I were given a chance to see what will happen there, I would trade everything I have to see if I made it./n/nI know that growing up is inevitable, but I can't help being afraid. I don't want to fail. I can't afford to fail. I can't handle rejection. The thought of not making it terrifies me. The uncertainty of the future haunts me. the fear of failure paralyzes me./n/nI know that life is bigger than failures and rejections. I know that those things wouldn't define me. I know that the world is big and full of opportunities and I shouldn't let those decide my fate, but still, I am afraid—so afraid./n/nWhat if I don't make it? What if all my efforts, all my hard work, lead to nothing? these thoughts swirl in my mind, keeping me awake at night. I wish i could find the courage to face these fears head-on, to embrace the unknown with open arms. but right now, all I can do is keep trying, keep pushing forward, and hope that somehow, I will find my way."
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
            {"role": "user", "content": user_message(False, "embrace and express their emotions without shame, especially when hurt.")},
            {"role": "assistant", "content": """```json {
                    "title": "in a world that’s obsessed with telling people to “get over it,” i hope you let yourself go through it instead",
                    "subtitle": "don’t let anyone convince you that your pain only counts if they say it does",
                    "tags": "Writing,Life,Mental Health,Relationships,Books",
                    "image": "flower vase aesthetic",
                    "body": "# don’t let anyone convince you that your pain only counts if they say it does/n/nFeel it. Say something. Make it known./n/nYou’re not too much for feeling deeply. You’re not being dramatic for flinching at the words they said in passing as if their sharpness couldn’t possibly reach you. As if you’re expected to swallow it whole and keep smiling./n/nBut you don’t have to./n/nYou are allowed to feel the sting. To let it sit in your chest and make it hard to breathe for a while. You are allowed to pause, to cry, to tremble, to ask why would you say that to me?/n/nBecause it hurt. And that matters./n/nWe live in a world that teaches us to shrink our reactions to fit other people’s comfort. To play it cool. To laugh it off. To keep it together, even when we are quietly falling apart. But you weren’t made to be a container for other people’s damage. You weren’t meant to numb your own feelings just so someone else doesn't have to confront the harm they’ve caused./n/nTake it personally if it was personal./n/nLet your silence break. Let your voice rise. Let your face show the things they said were “not a big deal.” Let them see the consequence of carelessness. Let them know that words do land somewhere. That tone matters. That jokes can wound. That passing comments don’t always pass./n/nYou are not overreacting. You are reacting. That’s different./n/nYou are not angry for no reason. You are angry because there was a reason, even if no one else wants to name it./n/nAnd no, you don’t have to keep explaining why something hurts just because they can’t — or won’t — understand. Your emotions are not a court case that needs proof. Sometimes, you felt it is all the explanation there is. And that is enough./n/nYou are not difficult for having limits. You are not wrong for feeling things deeply. You are not weak for needing time to recover./n/nYou are human./n/nAnd in a world that’s obsessed with telling people to “get over it,” I hope you let yourself go through it instead./n/nFeel it all. Loudly, if you must. Quietly, if you prefer. But don’t let anyone convince you that your pain only counts if they say it does./n/nIt counts because you felt it./n/nIt counts because it left a mark./n/nAnd you, even in the thick of your anger or ache or sorrow—you count, too."
                }```"""
            },
            {"role": "user", "content": user_message(False, "embrace gentleness and compassion in a world that often values hardness and judgment.")},
            {"role": "assistant", "content": """```json {
                    "title": "may you have a gentle heart so you don’t see the world with judgment and heavy heart",
                    "subtitle": "may you look at the world and not see strangers, but stories. not enemies, but people trying, hurting, hoping. people, like you, who just want to be okay.",
                    "tags": "Writing,Life,Mental Health,Relationships,Books",
                    "image": "water in pond aesthetic",
                    "body": "may you look at the world and not see strangers, but stories. not enemies, but people trying, hurting, hoping. people, like you, who just want to be okay./n/nThere is a kind of tiredness that doesn’t come from the body. A heaviness that sits in your chest when you’ve carried too many expectations, too many disappointments, too many sharp-edged stories you believed too quickly. The kind of tired that builds from looking at the world and seeing everything wrong first./n/nWe are taught, in little ways, to guard ourselves. To look with suspicion before curiosity. To protect before we understand. Somewhere along the way, kindness became weakness, and softness became something to outgrow./n/nBut I hope you unlearn that./n/nI hope you remember that having a gentle heart is not about being naïve. It’s not about ignoring what’s broken. It’s about choosing not to become bitter because of it. It’s about seeing the cracks and still believing in the light that can pass through./n/nIt’s easy to judge what we don’t understand. Easier to label than to listen. But I hope you find it in yourself to pause before you speak, to look before you assume. To give people the grace you wish someone had given you when you were messy, confused, or halfway through becoming someone better./n/nSome people are doing the best they can, and their best won’t always look like yours./n/nSome people are carrying things you’ll never see./n/nAnd maybe that’s reason enough to soften your gaze./n/nThere is already so much hardness in this world —too many cold shoulders, too many harsh words spoken without care. Be the place where gentleness still exists. Be someone who asks questions instead of offering conclusions. Someone who holds space instead of building walls./n/nA gentle heart does not mean you let the world walk over you. It means you walk through the world without adding to its pain. It means you choose compassion over cruelty, even when cruelty feels easier. Even when you are hurting too./n/nBecause maybe the goal is not to be untouched by the world—but to remain kind despite it./n/nLet your gentleness be a rebellion./n/nLet it be the quiet proof that softness can survive anything. Let it be your offering to a world that forgets, too often, how healing it is to be seen without judgment./n/nAnd when the weight feels like too much to carry—your own, or someone else’s—I hope you give yourself permission to rest, not harden. To breathe before reacting. To feel before deciding./n/nMay you look at the world and not see strangers, but stories. Not enemies, but people trying, hurting, hoping. People, like you, who just want to be okay./n/nAnd may your heart stay soft enough to understand that being human has always been hard—but it’s also beautiful, if you know where to look."
                }```"""
            },
            {"role": "user", "content": user_message(False, "love is not always expressed through action.")},
            {"role": "assistant", "content": """```json {
                    "title": "i don’t really believe in “if they wanted to, they would” anymore",
                    "subtitle": "what if they wanted to but they couldn’t?",
                    "tags": "Writing,Life,Mental Health,Relationships,Books",
                    "image": "london scenery",
                    "body": "## what if they wanted to but they couldn’t?/n/n“If they wanted to, they would.”/n/nI used to say that, too. Like it was the answer to every half-love, every message left on seen, every unfinished story. It sounds clean. Sharp. Too sharp, even — like it was made to slice through confusion and leave only certainty behind./n/nBut love isn’t clean. And people — people are anything but simple./n/nBecause maybe they did want to. Maybe they still do. But desire doesn’t always lead to action. Not because it isn’t real, but because it isn’t always easy./n/nSometimes, people want to love you right but they don’t know how. Sometimes they want to show up but their legs are shaking. Sometimes they want to choose you but they’re choosing survival first./n/nNo one ever talks about the weight of fear. How some hands tremble too hard to reach out. How timing can betray even the sincerest of intentions. How someone might carry years of silence in their chest and saying your name would mean breaking through every wall they built to feel safe./n/nThat takes time. That takes healing. And sometimes, healing doesn’t happen fast enough./n/nAnd maybe that’s what hurts the most — not the absence, but the knowing./n/nKnowing they thought of you and still didn’t come./n/nKnowing they cared and still disappeared./n/nKnowing they wanted to — and still, they didn’t./n/nBut I don’t think that makes them cruel./n/nI think that just makes them human./n/nI’ve met people who loved me quietly from the sidelines. People who wanted to stay but didn’t know how. I’ve been that person too — standing at the edge of something good, something warm, something whole — and choosing to walk away. Not because I didn’t want it. But because I wasn’t sure if I could hold it without breaking it./n/nThere were people I wanted to stay for, but I left./n/nNot out of indifference, but out of fear. Fear of being too much. Fear of not being enough. Fear of being the reason someone else starts to ache./n/nAnd yet, I blamed myself when others did the same. I told myself, “If they wanted to, they would.” As if all hearts beat with the same rhythm. As if every soul learns love the same way./n/nBut we don’t./n/nSome people show love in loud, obvious ways./n/nOthers — only in stutters. In half-smiles. In almosts./n/nIn I-wanted-to-but-I-couldn’t./n/nIn I’m-here-but-I-don’t-know-how-to-stay./n/nIt’s easier to believe they didn’t care. That they never meant it. But the truth is heavier and softer: sometimes, wanting isn’t loud. Sometimes, it’s scared. Sometimes, it leaves./n/nIf they wanted to, maybe they couldn’t./n/nIf they wanted to, maybe the timing wasn’t right./n/nIf they wanted to, maybe the world didn’t give them the chance to./n/nWe are all fighting battles no one sees. We are all learning how to reach without flinching. To love without running. To stay without trembling./n/nThat phrase — if they wanted to, they would —assumes that love is always brave. But love, in real life, is often full of fear. Of trying and failing. Of meaning well but still falling short./n/nMaybe they wanted to./n/nMaybe they did./n/nBut they didn’t, they couldn’t./n/nAnd maybe that doesn’t make them heartless./n/nIt just makes them human."
                }```"""
            },
            {"role": "user", "content": user_message(False, "we often give others the love, belief, and kindness we struggle to give ourselves.")},
            {"role": "assistant", "content": """```json {
                    "title": "i hate how easy it is for me to believe in other people, but not in myself",
                    "subtitle": "maybe i’ve built a life around being a mirror for others, and somewhere in the reflection, i forgot how to see myself",
                    "tags": "Writing,Life,Mental Health,Relationships,Books",
                    "image": "face in the mirror",
                    "body": "## maybe i’ve built a life around being a mirror for others, and somewhere in the reflection, i forgot how to see myself/n/nI hate how easy it is for me to believe in other people, but not in myself. /n/nIt’s almost an instinct — how I can look at someone and see their light even when they’re drowning in doubt. How I can tell them, with complete conviction, that they’re capable, strong, worthy. I can name their softness without making it sound like weakness. I can remind them that they’re allowed to take up space, allowed to rest, allowed to be. /n/nBut when it comes to me, I hesitate. The words don’t land the same. The grace I give to others feels too heavy when I try to carry it for myself. Like it wasn’t made for me. Like I’m borrowing something I don’t deserve. /n/nIt’s strange — how I can recognize potential in everyone else but feel like mine always comes with a question mark. How I can cheer for someone else’s almosts, but tear apart my own. /n/nMaybe it’s because I learned to be the helper. The listener. The one who holds. And somewhere along the way, I convinced myself that belief is something you give, not something you keep. /n/nBut the truth is: I give away the kindness I never learned how to give to myself. And it shows. It shows in how quickly I forgive others, but not my own missteps. In how I lift people up, then go home and wonder why I feel so empty. In how I tell others they’re enough — over and over — while secretly asking myself if I ever will be. /n/nI don't know why it's easier to root for everyone else. Maybe I think they deserve it more. Maybe it's safer to pour love outward than try to plant it inward. Maybe I've built a life around being a mirror for others, and somewhere in the reflection, I forgot how to see myself. /n/nBut I want to learn. Not just how to believe in myself, but how to stay with myself. How to offer my own name the same softness I’ve wrapped around everyone else’s. How to tell the mirror, one day, “You, too.” /n/nBecause if I can believe in people who are still figuring it out, then maybe, I can also try to believe in the only person who’s been here the whole time: me."
                }```"""
            },
            {"role": "user", "content": user_message(False, "Living fully, with intention and presence.")},
            {"role": "assistant", "content": """```json {
                    "title": "to leave without regrets? to live without regrets.",
                    "subtitle": "to leave without regrets, you have to live like your life belongs to you.",
                    "tags": "Writing,Life,Mental Health,Relationships,Books",
                    "image": "aesthetic girl picture",
                    "body": "## to leave without regrets, you have to live like your life belongs to you./n/nPeople talk a lot about how to die well. How to leave without loose ends, without bitterness, without regret sitting heavy on the chest. But no one ever really tells us how to live that way./n/nHow do you live in a way that makes leaving easier?/n/nMaybe it begins with the things that seem invisible until they’re not. The morning light on your windowsill. The way your friend remembers your coffee order. The long walks you take just to clear your head. The apology you gave even when your pride didn’t want to. The nights you let yourself cry. The days you chose to try again./n/nMaybe it’s not always about chasing some kind of grand purpose or endless success. Maybe it’s about noticing. Noticing the way your heart steadies when you’re doing something that matters, even if it’s quiet and no one’s watching. Noticing the way your voice shakes when you're honest. Noticing what makes you feel alive, and making more room for that./n/nLiving without regrets isn’t the absence of mistakes. It’s having the courage to keep showing up, even after you’ve made them. It’s standing in front of the mirror and choosing not to look away from the version of yourself that’s still learning./n/nWe think regret comes from failure. But it often comes from absence. From not showing up for the people we love. From abandoning ourselves in moments we should’ve stood still. From silencing our dreams before they had a chance to speak. From saying “maybe later” too many times until there’s no later left./n/nTo live without regrets is not to get everything right. It’s to live as if you’re already aware this ends. And yet you keep loving, anyway. You keep trying, anyway. You keep making room for joy even on the days when it doesn’t knock. You keep choosing yourself, even when the world forgets to./n/nWe always ask: How do I leave well? But the better question might be: How do I stay well while I’m here?/n/nBecause leaving without regrets begins with living with presence./n/nIt means meaning your “I love you”s. It means taking the photo. Writing the letter. Forgiving. Walking away when it’s time. Beginning again. Letting people in. Letting yourself feel things fully, even when they hurt. Especially when they hurt./n/nIt means asking yourself often, If this was the last time — would it be enough?/n/nTo leave without regrets, you have to live like your life belongs to you./n/nNot to fear. Not to perfection. Not to what-ifs./n/nTo you./n/nAnd maybe, if you can manage that — if you can live like your heart is yours and your time is real and your voice is worth hearing — then when it’s time to go, it won’t feel like a theft./n/nIt will feel like the closing of a chapter you wrote with your own hands. And in the silence that follows, you’ll know: I was here. I lived. And I meant it."
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
