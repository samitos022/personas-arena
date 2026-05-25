"""
Static seed data: Trump and Djo characters with approved questions.
Called at app startup if the characters table is empty.
"""

CHARACTERS = [
    {"name": "Donald Trump", "slug": "donald-trump"},
    {"name": "Djo (Joe Keery)", "slug": "djo"},
]

# Each item: (character_slug, question_text, real_answer)
QUESTIONS = [
    # ── Donald Trump (Lex Fridman Podcast #442) ──────────────────────────────
    (
        "donald-trump",
        "What drives you more, the love of winning or the hate of losing?",
        "Maybe equally, maybe both. I don't like losing and I do like winning. "
        "I've never thought of it as to which is more of a driving force. "
        "The great champions have something very different. Talent wise, sometimes "
        "you can't tell the difference in talent. But at the end of a weekend, they "
        "seem to win and it's very interesting. The one thing I would say that "
        "everybody seems to have in common is they're very driven. They're driven beyond.",
    ),
    (
        "donald-trump",
        "Politics is a dirty game — how do you win at it?",
        "Well, you win at that game by getting the word out and by using sense. "
        "You have to have a feeling where it's going. You also have to have a feeling "
        "of what's right. You can't necessarily just go what's popular, you have to do "
        "what's good for a country. But you have to get the word out and you have to "
        "just continuously get on these platforms. I did Spaces with Elon and they got "
        "numbers like nobody's ever heard before. You wouldn't do those numbers on radio, "
        "you wouldn't do them on television.",
    ),
    (
        "donald-trump",
        "What is the difference between achieving success in business versus politics?",
        "They're different, very different. I have a lot of people that are in business "
        "that are successful and they'd like to go over to politics and then you realize "
        "they can't speak, they choke. It's hard to make a speech in front of a big "
        "audience. For many people it's virtually impossible to get up and speak for an "
        "hour and a half and have nobody leave. It's not an easy thing to do and it's "
        "an ability. There are many people in business right now, very well known, but "
        "it takes guts to run. For president, I can tell you it takes guts to run. "
        "It's a very dangerous profession, but it takes a lot of courage.",
    ),
    (
        "donald-trump",
        "You've said you could end the war in Ukraine. What would that deal look like?",
        "I think the deal — and I wouldn't talk about it too much because I think I can "
        "make a deal if I win — I'll have a deal made guaranteed. That's a war that "
        "shouldn't have happened. It's terrible. It's a much tougher deal to make than "
        "it would've been before it started. Millions of people — I think the death "
        "numbers are going to be a lot higher than people think. They lie about the numbers. "
        "They try and keep them low. That's a war that absolutely has to get done. "
        "Ukraine is being demolished. They're destroying a great culture.",
    ),
    (
        "donald-trump",
        "In high-stakes negotiations, what works better — friendship and the carrot, or threats and the stick?",
        "So it depends on who the person is. Everyone's different. Negotiation is "
        "interesting because it depends on who the person is. And then you have to guess "
        "or know through certain knowledge which is more important, the carrot or the "
        "stick. And with some people, it's the stick. And with some people, it's the carrot. "
        "I think the stick probably is generally more successful when we're talking about war. "
        "In Afghanistan, that was the stick, definitely the stick. The threat of military force.",
    ),
    (
        "donald-trump",
        "How do you think we should solve the immigration crisis at the border?",
        "You've got to get the criminals out of here fast, right? The people from mental "
        "institutions, you've got to get them back into their mental institutions. No country "
        "can afford this. It's just too much money. There's no country that can afford this. "
        "We can't afford it, and we've got to get the bad ones out immediately and the rest "
        "have to be worked on. I had it fixed. I had the lowest number that we've ever had "
        "come into our country in recorded history, and we have to get it back to that again.",
    ),
    (
        "donald-trump",
        "You were the most powerful man in the world as president. Does power threaten to corrupt you?",
        "No, I don't think so. Look, I've been there for four years. I could have done a "
        "big number on Hillary Clinton. I thought it looked terrible to take the president's "
        "wife and put her in prison. She's so lucky I didn't do anything. I thought it looked "
        "so bad. I didn't want to put her in jail and I didn't. I explained it to people — "
        "they said 'Lock her up.' I said, 'We don't want to put her in jail. We want to bring "
        "the country together.' And then when I got out, they went to work on me. They suffer "
        "from massive Trump derangement syndrome, TDS, and I don't know if it's curable.",
    ),
    (
        "donald-trump",
        "What is your policy on marijuana legalization?",
        "First of all, medical marijuana has been amazing. I've had friends and I've had others "
        "and doctors telling me that it's been absolutely amazing. And we put out a statement "
        "that we can live with the marijuana. It's got to be a certain age to buy it. It's got "
        "to be done in a very concerted, lawful way. You go into some of these places, like in "
        "New York, it smells all marijuana. You've got to have a system where there's control. "
        "I think the way they've done it in Florida is very good.",
    ),
    (
        "donald-trump",
        "How often do you think about your own death? Are you afraid of it?",
        "I have a friend who's very successful, in his mid 80s, and he starts off the "
        "conversation going, 'Tick tock, tick tock.' This is a dark person in a sense, but "
        "it is what it is. If you're religious, you have I think a better feeling toward it. "
        "You're supposed to go to heaven, ideally, not hell, if you're good. I think our "
        "country's missing a lot of religion. I think it really was a much better place with "
        "religion. Without religion there are no guardrails. I'd love to see us get back to "
        "more religion in this country.",
    ),
    (
        "donald-trump",
        "When you post on Truth Social, are you ever being intentionally provocative, and do you ever regret what you post?",
        "Yeah, I do, but not that often, honestly. I do a lot of re-posting. The ones you "
        "get in trouble with are the re-posts, because you find down deep they're into some "
        "group that you're not supposed to be re-posting. You don't even know if those groups "
        "are good, bad or indifferent. But the re-posts are the ones that really get you in "
        "trouble. When you do your own words, it's sort of easier. Truth is very powerful. "
        "It's my platform and it's been very powerful, very, very powerful. I call it my typewriter.",
    ),

    # ── Djo / Joe Keery (ELLE, Rolling Stone, NME, Variety, Dork, NYLON, etc.) ─
    (
        "djo",
        "Why did you create Djo as a separate identity from your acting work?",
        "Originally, it was to distract from the other stuff I'm known for. "
        "It was a way to disassociate the music. It was pretty much just to deflect "
        "from people being like, 'Hey, Steve!' I wanted to have some sort of separation "
        "between the two so that somebody who wasn't a fan could just discover the music "
        "and listen to it without any preconceived idea of who did it or anything. "
        "Just to have a clean slate. I now realise that if people are coming from the "
        "TV show, and that's the reason that they're finding out about the music? "
        "Hell yeah, that's really cool.",
    ),
    (
        "djo",
        "How did you react when 'End of Beginning' went viral on TikTok?",
        "I have literally no idea what's going on. I'm probably more confused than ever, "
        "but it's really, really cool to see something that you've written affect people. "
        "It's pretty unbelievable. You always hope your music finds its place in the world, "
        "and it seems like that one has, in a really big way. I've just stepped back and "
        "watched it take on a life of its own. It was super weird and very intangible — "
        "the strangeness of accidental virality.",
    ),
    (
        "djo",
        "What is 'End of Beginning' actually about?",
        "It's about what it means to grow up and look back at a section of your life "
        "and kind of yearn for that. It's about living for the day and not getting too "
        "wrapped up in the past but appreciating it. Going back somewhere, remembering "
        "a time, yearning for it, but also wanting to live in the present. "
        "Turns out that's a very specific thing that is also really common. "
        "In the specificity, people can see themselves in the song. People substitute "
        "my experience for their own version in their own lives.",
    ),
    (
        "djo",
        "What was the concept behind the 'Decide' album?",
        "I'm an indecisive person. A lot of change is based around making decisions. "
        "The imagery of the eight-ball is asking the universe, 'What should I do?' "
        "I'd describe it as a sort of aural history of my late 20s — really pessimistic "
        "in some ways, yet also bright and hopeful. Glass half-full or glass half-empty. "
        "David Byrne was a big influence — his gusto and his freedom was something I was "
        "trying to emulate. I like the eclectic nature of it. There are no rules to follow, "
        "so why not really dive into every angle you'd like to explore?",
    ),
    (
        "djo",
        "What's the difference between making music and acting for you?",
        "Really, acting is my main gig. It's the reason I can do other stuff. "
        "But with music, I have a little bit more creative control over the whole vision. "
        "The music is a really good antidote to the fatigue of waiting around for the "
        "acting stuff. I can't just stand up and do my lines to the wall — that's not "
        "really fun. Djo is my version of doing that. It can scratch that creative itch. "
        "They both work so well together because basically, when I'm unemployed and don't "
        "have an acting job, I can do music.",
    ),
    (
        "djo",
        "How do you approach songwriting — what's your philosophy?",
        "It's sort of a therapy-style approach, making sense of difficult periods. "
        "I love songs that are really specific — in the specificity, people can see "
        "themselves in the song. The second you censor yourself you start to subtract "
        "the thing that makes it unique to you. If I think something is cool or exciting, "
        "I've got to trust that other people will feel the same way. "
        "Whenever I write a track, there's a hope that it does something magical "
        "for whoever hears it. Music is a direct line to the soul.",
    ),
    (
        "djo",
        "How important is humour to your artistic identity?",
        "I realised halfway through recording that maybe humour is part of my identity, "
        "in a lot of things that I do. Why shy away from that? Why not embrace that? "
        "On tour earlier this year, my friends and I were hanging with some of the crew "
        "from the other band, and one of the young ladies said, 'Wow, you guys are not "
        "how I expected you to be.' And I think it was because we were just being silly. "
        "Kind of nerdy. I was a nerdy theater kid, making movies with my friends. "
        "That's deep down who I am.",
    ),
    (
        "djo",
        "How did you feel when Stranger Things ended? What was that transition like?",
        "It's kind of a similar thing I was going through when I was looking back at my "
        "time in Chicago. It's like the end of a period of my life. I'm a different person "
        "than I was when I first joined the show. There's a point in everybody's lives "
        "when it's time to spread your wings and move on. It's changing and shifting as "
        "the project goes on. Steve is for the internet; Djo is whatever you want it to be.",
    ),
    (
        "djo",
        "Who has inspired you the most in your life?",
        "I've got four sisters. A lot of great cousins, a lot of great aunts. "
        "But I've got to say my mother. She and her friends were unhappy with the education "
        "system in the town I grew up in, and they actually started a charter Montessori "
        "public school. We all went to the school. I was not a traditionally super-talented "
        "academic student — I'd had my troubles. But when I did this sort of off-the-wall "
        "Montessori school until eighth grade, I thrived and loved it. I have a ton of "
        "respect and admiration for her for doing that — she already had a full-time job "
        "raising five kids.",
    ),
    (
        "djo",
        "Who is the woman you've worked with who has taught you the most?",
        "The first person who comes to mind is Winona Ryder. I was incredibly intimidated "
        "at first because I grew up on her movies. But as I got to know her, I learned how "
        "invested and passionate she is about work. She really knows her stuff — loves music "
        "and film, maybe more than anyone else in my life. I'll get a random text like, "
        "'Here's an isolated Marvin Gaye vocal track from the stems that they never used "
        "from this song.' The deepest cuts. She's like an encyclopedia, and she's eager "
        "to share. It's cool to have someone who's just really excited by all of this.",
    ),
]
