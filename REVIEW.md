# Review sheet

All 180 shipping demos, grouped by family and difficulty, with what the two listening audits reported. Anything listed here can be removed by deleting its id from `curation/06_selected.jsonl` and re-running `tools/07_export.py`.


## Speech Content — L1

### `content-l1-real-emotion`

- **Question** How does the speaker sound?
- **Answer** C. sad
- **Audio** [assets/audio/content/content-l1-real-emotion/clip.wav](assets/audio/content/content-l1-real-emotion/clip.wav) · 2.27s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A woman quietly whispers the word 'No'.
- **Why the answer stands** The report describes the speaker's tone as 'resigned', which supports the claimed answer of 'sad' and is not better described by the other options.
- **Difficulty** score 0.1538 (auditor answered 4/5 blind, training solver 0.8333333333333334)

### `content-l1-dialogue-qa`

- **Question** What is the final plan decided at the end?
- **Answer** C. To switch to a new teacher and join a Saturday class
- **Audio** [assets/audio/content/content-l1-dialogue-qa/clip.wav](assets/audio/content/content-l1-dialogue-qa/clip.wav) · 16.66s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man complains about his fingers hurting from learning guitar, and a woman advises him on his practice and suggests changing teachers next month, set against a background sound of heavy rain.
- **Why the answer stands** The transcribed dialogue and summary show Speaker 2 advising Speaker 1 to change teachers next month and recommending the Saturday class, which directly supports Option C.
- **Difficulty** score 0.2071 (auditor answered 5/5 blind, training solver 1.0)

### `content-l1-content-qa`

- **Question** Why was the speaker annoyed?
- **Answer** B. The sauce was too salty
- **Audio** [assets/audio/content/content-l1-content-qa/clip.wav](assets/audio/content/content-l1-content-qa/clip.wav) · 28.18s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A woman describes her disappointing experience trying a new pasta recipe that turned out too salty, set to background acoustic guitar music.
- **Why the answer stands** The report explicitly states that the speaker was annoyed because the recipe turned out too salty despite her following the steps exactly.
- **Difficulty** score 0.1516 (auditor answered 5/5 blind, training solver 1.0)

### `content-l1-real-dialogue-qa`

- **Question** Why does the second speaker say 'Would you stop that!'?
- **Answer** D. Because the first speaker is making a wrong assumption.
- **Audio** [assets/audio/content/content-l1-real-dialogue-qa/clip.wav](assets/audio/content/content-l1-real-dialogue-qa/clip.wav) · 13.1s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man expresses insecurity about a woman talking to Richard, but a female companion reassures him that the woman loves him.
- **Why the answer stands** The report shows Speaker 1 making an insecure assumption about a woman talking to Richard, which Speaker 2 immediately refutes by reassuring him that the woman actually loves him, confirming that Speaker 1's assumption was incorrect.
- **Difficulty** score 0.0863 (auditor answered 5/5 blind, training solver 0.8333333333333334)

### `content-l1-dialogue-emotion`

- **Question** Which speaker sounds sad?
- **Answer** B. the man
- **Audio** [assets/audio/content/content-l1-dialogue-emotion/clip.wav](assets/audio/content/content-l1-dialogue-emotion/clip.wav) · 28.77s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A female and a male speaker alternate reading short Chinese sentences, with the female sounding neutral and the male sounding melancholic.
- **Why the answer stands** The report states that the male speaker (Speaker 2) speaks with a melancholic, lonely, and reflective emotion, which directly supports the claimed answer that the man sounds sad.
- **Difficulty** score 0.1043 (auditor answered 5/5 blind, training solver 0.8333333333333334)

### `content-l1-real-dialogue-emotion`

- **Question** Identify the emotion of each speaker in the conversation.
- **Answer** D. the first speaker sounds happy, the second speaker sounds happy
- **Audio** [assets/audio/content/content-l1-real-dialogue-emotion/clip.wav](assets/audio/content/content-l1-real-dialogue-emotion/clip.wav) · 11.6s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man and a woman share a quiet, intimate moment, reflecting breathlessly on how they may have just changed their lives and started a family.
- **Why the answer stands** The report describes Speaker 1 as having 'content satisfaction' and Speaker 2 as having 'emotional warmth' in a 'quiet, intimate moment', which supports both being described as 'happy' rather than 'excited' or 'neutral'.
- **Difficulty** score 0.0845 (auditor answered 5/5 blind, training solver 0.8333333333333334)


## Speech Content — L2

### `content-l2-dialogue-qa`

- **Question** Which speaker is happy about the phone breaking?
- **Answer** C. The first speaker
- **Audio** [assets/audio/content/content-l2-dialogue-qa/clip.wav](assets/audio/content/content-l2-dialogue-qa/clip.wav) · 50.34s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A family argues about a young man's broken phone and tablet before a younger sibling assertively decides they will get the phone repaired today.
- **Why the answer stands** The report explicitly transcribes Speaker 1 (the first speaker) saying 'I'm actually thrilled my old phone finally broke.'
- **Difficulty** score 0.2617 (auditor answered 5/5 blind, training solver 1.0)

### `content-l2-content-qa`

- **Question** Why did the speaker contact the building manager?
- **Answer** B. Because Dave ignored the knocks and turned up the stereo
- **Audio** [assets/audio/content/content-l2-content-qa/clip.wav](assets/audio/content/content-l2-content-qa/clip.wav) · 18.16s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man narrates a story about his neighbor making noise late at night, set against a background of applause and cheering.
- **Why the answer stands** The report supports the claimed answer because the transcript states the speaker knocked twice but the neighbor turned up the stereo just before the speaker called the manager, despite the minor name discrepancy of 'Dave' instead of 'Gabe'.
- **Difficulty** score 0.2865 (auditor answered 5/5 blind, training solver 1.0)

### `content-l2-real-dialogue-qa`

- **Question** Who says 'Oh it was perfect! I mean it really felt like he was my friend again'?
- **Answer** B. The third speaker
- **Audio** [assets/audio/content/content-l2-real-dialogue-qa/clip.wav](assets/audio/content/content-l2-real-dialogue-qa/clip.wav) · 25.91s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A comedic dialogue from a television show where a couple's romantic moment is interrupted by an excited friend sharing successful advice, only to quickly dodge a follow-up question.
- **Why the answer stands** The report identifies Phoebe as the third speaker in the dialogue and transcribes her as saying the line in question.
- **Difficulty** score 0.2549 (auditor answered 5/5 blind, training solver 0.5)

### `content-l2-real-dialogue-emotion`

- **Question** Which speaker sounds happy?
- **Answer** A. the first speaker
- **Audio** [assets/audio/content/content-l2-real-dialogue-emotion/clip.wav](assets/audio/content/content-l2-real-dialogue-emotion/clip.wav) · 10.88s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A woman enthusiastically says 'Great!' and a man explains that he wants to make sure their personalities match before making a decision, mentioning he has prepared a test, with the first part of the exchange repeating due to an audio loop.
- **Why the answer stands** The report states that Speaker 1 (the first speaker) sounds enthusiastic and cheerful, which supports the claimed answer that the first speaker sounds happy, while Speaker 2 is described as calm, friendly, and deliberate.
- **Difficulty** score 0.2376 (auditor answered 5/5 blind, training solver 0.5)

### `content-l2-long-content-qa`

- **Question** What does the speaker imply about the possibility of going back to Nonna's Table?
- **Answer** D. They are skeptical about the service.
- **Audio** [assets/audio/content/content-l2-long-content-qa/clip.wav](assets/audio/content/content-l2-long-content-qa/clip.wav) · 51.34s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man describes a disappointing experience trying to eat at a new restaurant called Nonna's Table, which led him and his sister to dine at an Italian bistro on Fifth Street instead.
- **Why the answer stands** The speaker's statement that he is hesitant to try Nonna's again 'after that mess' directly supports his skepticism about the restaurant's service.
- **Difficulty** score 0.2769 (auditor answered 5/5 blind, training solver 0.5)

### `content-l2-speech-semantic-qa-real`

- **Question** Listen to the passage. Which of the following is NOT mentioned in the passage?
- **Answer** C. A crowd of onlookers
- **Audio** [assets/audio/content/content-l2-speech-semantic-qa-real/clip.wav](assets/audio/content/content-l2-speech-semantic-qa-real/clip.wav) · 11.92s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A female narrator reads a dramatic excerpt from a story over a background sound of a rhythmic clanking carriage or train.
- **Why the answer stands** The transcription in the report explicitly mentions a rock, the Committee of Public Safety, and a hard bed of stone, but does not mention a crowd of onlookers, confirming that C is the correct answer.
- **Difficulty** score 0.2396 (auditor answered 5/5 blind, training solver 1.0)


## Speech Content — L3

### `content-l3-dialogue-qa`

- **Question** What is the man's plan at the end of the conversation?
- **Answer** D. To get an emergency light and order takeout
- **Audio** [assets/audio/content/content-l3-dialogue-qa/clip.wav](assets/audio/content/content-l3-dialogue-qa/clip.wav) · 32.86s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A frustrated woman complains about a power outage, while a calm man explains the delay in power restoration and offers solutions like using an emergency light and ordering takeout.
- **Why the answer stands** The report's transcript and summary explicitly state that the man plans to get an emergency light from his car and order takeout, which directly supports option D.
- **Difficulty** score 0.3309 (auditor answered 5/5 blind, training solver 1.0)

### `content-l3-speech-semantic-qa-real`

- **Question** According to the speaker, Who does "his" refer to in the passage?
- **Answer** D. The person holding the paper
- **Audio** [assets/audio/content/content-l3-speech-semantic-qa-real/clip.wav](assets/audio/content/content-l3-speech-semantic-qa-real/clip.wav) · 10.46s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man reads a dramatic narrative passage over a steady hip-hop instrumental beat.
- **Why the answer stands** The transcribed text in the report states that 'The sheet of paper covered with circles dropped out of his fingers', which directly supports that 'his' refers to the person holding the paper.
- **Difficulty** score 0.3447 (auditor answered 5/5 blind, training solver 0.75)

### `content-l3-real-dialogue-emotion`

- **Question** Which speaker sounds surprised?
- **Answer** A. the first speaker
- **Audio** [assets/audio/content/content-l3-real-dialogue-emotion/clip.wav](assets/audio/content/content-l3-real-dialogue-emotion/clip.wav) · 2.6s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man speaks a single questioning sentence: 'Well yeah, that, that's it?'
- **Why the answer stands** The report describes a single speaker who delivers his line with a tone of mild surprise, which supports the claim that the first speaker sounds surprised.
- **Difficulty** score 0.3077 (auditor answered 4/5 blind, training solver 0.5)

### `content-l3-content-qa`

- **Question** What happened right before the speaker was about to leave?
- **Answer** D. Her sister called from the airport
- **Audio** [assets/audio/content/content-l3-content-qa/clip.wav](assets/audio/content/content-l3-content-qa/clip.wav) · 26.14s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man recounts missing his dentist appointment to pick up his sister from the airport, which ultimately made his week despite his initial annoyance.
- **Why the answer stands** The transcript directly supports the claimed answer, noting that the speaker was just about to leave when his sister called him from the airport.
- **Difficulty** score 0.3179 (auditor answered 5/5 blind, training solver 1.0)

### `content-l3-real-dialogue-qa`

- **Question** Why does the second speaker offer for the first speaker to stay with Rachel and them?
- **Answer** A. Because the first speaker's grandmother is too loud at night
- **Audio** [assets/audio/content/content-l3-real-dialogue-qa/clip.wav](assets/audio/content/content-l3-real-dialogue-qa/clip.wav) · 19.41s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A woman tells a humorous story about her grandmother to a laughing audience, leading a friend to offer her a place to stay.
- **Why the answer stands** The transcribed speech in the report explains that the grandmother and her boyfriend are very loud in bed, which directly supports the claimed answer that they are too loud at night.
- **Difficulty** score 0.3243 (auditor answered 5/5 blind, training solver 0.3333333333333333)

### `content-l3-dialogue-emotion`

- **Question** Which speaker sounds happy?
- **Answer** A. the man
- **Audio** [assets/audio/content/content-l3-dialogue-emotion/clip.wav](assets/audio/content/content-l3-dialogue-emotion/clip.wav) · 18.1s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** Four different speakers take turns reading short, unrelated sentences with varying tones and delivery styles.
- **Why the answer stands** The report states that Speaker 1 (male) speaks in a cheerful, pleasant tone and Speaker 3 (male) speaks in an excited whisper, while both female speakers are neutral, supporting the claim that the man sounds happy.
- **Difficulty** score 0.3228 (auditor answered 5/5 blind, training solver 0.3333333333333333)


## Speech Content — L4

### `content-l4-real-dialogue-emotion`

- **Question** Identify the emotion of each speaker in the conversation.
- **Answer** A. the first speaker sounds angry, the second speaker sounds angry
- **Audio** [assets/audio/content/content-l4-real-dialogue-emotion/clip.wav](assets/audio/content/content-l4-real-dialogue-emotion/clip.wav) · 5.29s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A brief comedic exchange occurs where a woman accuses a man of touching her, he defensively claims she touched him first, and another woman claims that touching him is her job.
- **Why the answer stands** The report describes the first speaker as having an 'indignant' tone and the other female speaker as having an 'outraged' tone, both of which support the claimed answer that they sound angry.
- **Difficulty** score 0.3849 (auditor answered 5/5 blind, training solver 0.16666666666666666)

### `content-l4-dialogue-qa`

- **Question** Who first suggested going hiking?
- **Answer** A. The second speaker
- **Audio** [assets/audio/content/content-l4-dialogue-qa/clip.wav](assets/audio/content/content-l4-dialogue-qa/clip.wav) · 26.06s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** Four friends coordinate their plans for an early morning hike and brunch, adjusting their meeting time to 7:00.
- **Why the answer stands** The transcript shows Speaker B (the second speaker) is the first to mention hiking ('We're hiking Mount Echo at sunrise'), which supports the claimed answer.
- **Difficulty** score 0.3808 (auditor answered 5/5 blind, training solver 0.5)

### `content-l4-speech-semantic-qa-real`

- **Question** According to the speaker, What is the speaker most likely trying to do?
- **Answer** C. Explain why he noticed a freshman from another college.
- **Audio** [assets/audio/content/content-l4-speech-semantic-qa-real/clip.wav](assets/audio/content/content-l4-speech-semantic-qa-real/clip.wav) · 15.36s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man reads a passage in a formal tone against a background of continuous applause.
- **Why the answer stands** The transcribed speech explicitly states that the unusual name of the freshman at Westminster attracted his attention, which directly supports option C.
- **Difficulty** score 0.3484 (auditor answered 5/5 blind, training solver 0.75)

### `content-l4-content-qa`

- **Question** How much did the speaker pay as a deposit?
- **Answer** A. 108 euros
- **Audio** [assets/audio/content/content-l4-content-qa/clip.wav](assets/audio/content/content-l4-content-qa/clip.wav) · 22.51s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man enthusiastically explains the details of a hotel booking in Lisbon over a background of rhythmic hand clapping.
- **Why the answer stands** The report states the total cost was 540 euros and the deposit was 20%, which mathematically equals 108 euros (Option A).
- **Difficulty** score 0.4081 (auditor answered 5/5 blind, training solver 0.5)

### `content-l4-real-dialogue-qa`

- **Question** Which speaker corrects the other's pronunciation of a name?
- **Answer** D. The first speaker
- **Audio** [assets/audio/content/content-l4-real-dialogue-qa/clip.wav](assets/audio/content/content-l4-real-dialogue-qa/clip.wav) · 17.95s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** This is a comedic television clip of a traffic stop where a driver playfully teases a police officer, followed by a dramatic remark from a female passenger.
- **Why the answer stands** The report explicitly states that Speaker 1 (the first speaker) corrects Speaker 2, clarifying that his name is 'Petty' rather than 'Pretty'.
- **Difficulty** score 0.3996 (auditor answered 5/5 blind, training solver 0.16666666666666666)

### `content-l4-dialogue-emotion`

- **Question** Which speaker sounds angry?
- **Answer** B. the woman
- **Audio** [assets/audio/content/content-l4-dialogue-emotion/clip.wav](assets/audio/content/content-l4-dialogue-emotion/clip.wav) · 24.33s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A female speaker and a male speaker take turns reading short sentences, with the female expressing frustration and the male speaking in a neutral tone.
- **Why the answer stands** The report states that the female speaker delivers her lines with an annoyed, frustrated, and complaining tone, while the male speaker is calm and neutral, which supports the claim that the woman sounds angry.
- **Difficulty** score 0.4069 (auditor answered 5/5 blind, training solver 0.16666666666666666)


## Speech Content — L5

### `content-l5-dialogue-qa`

- **Question** According to the woman, why was the train delayed?
- **Answer** A. A tree fell on the tracks
- **Audio** [assets/audio/content/content-l5-dialogue-qa/clip.wav](assets/audio/content/content-l5-dialogue-qa/clip.wav) · 29.1s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A group of travelers at a train station discuss a train delay, correct the rumored cause of the delay, and decide to take a bus instead.
- **Why the answer stands** The report explicitly states that Speaker 3, who is identified as female, corrected Speaker 2 by noting that the announcement reported a tree fell on the tracks.
- **Difficulty** score 0.6364 (auditor answered 5/5 blind, training solver 0.0)

### `content-l5-speech-semantic-qa-real`

- **Question** Based on what is said in the recording: What does 'her' refer to in the passage?
- **Answer** D. The pilgrim ship
- **Audio** [assets/audio/content/content-l5-speech-semantic-qa-real/clip.wav](assets/audio/content/content-l5-speech-semantic-qa-real/clip.wav) · 15.88s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A male speaker reads a literary passage while loud yawning and groaning sounds are heard in the background.
- **Why the answer stands** The report contains the full transcription of the passage, which provides the necessary context to determine that 'her' refers to 'the pilgrim ship'.
- **Difficulty** score 0.5144 (auditor answered 5/5 blind, training solver 0.25)

### `content-l5-content-qa`

- **Question** What day did the speaker receive the invitation?
- **Answer** B. Saturday
- **Audio** [assets/audio/content/content-l5-content-qa/clip.wav](assets/audio/content/content-l5-content-qa/clip.wav) · 20.94s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man cheerfully shares his travel plans to attend a friend's wedding in Shanghai, accompanied by rhythmic hand clapping.
- **Why the answer stands** The transcribed speech explicitly states '上周六我收到一張請柬' (Last Saturday I received an invitation), which directly supports Option B.
- **Difficulty** score 0.4936 (auditor answered 5/5 blind, training solver 0.0)

### `content-l5-real-dialogue-qa`

- **Question** Who identifies the woman in the middle as Nana?
- **Answer** C. The third speaker
- **Audio** [assets/audio/content/content-l5-real-dialogue-qa/clip.wav](assets/audio/content/content-l5-real-dialogue-qa/clip.wav) · 25.7s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A group of friends are looking at old photographs of Monica's grandmother, noting the resemblance and commenting on the 'gang' she was with.
- **Why the answer stands** The transcript in the report shows that Monica, who is the third speaker, says 'Oh, that's Nana right there in the middle', which directly supports the claimed answer.
- **Difficulty** score 0.4854 (auditor answered 5/5 blind, training solver 0.0)

### `content-l5-real-dialogue-emotion`

- **Question** Identify the emotion of each speaker in the conversation.
- **Answer** B. the first speaker sounds surprised, the second speaker sounds surprised
- **Audio** [assets/audio/content/content-l5-real-dialogue-emotion/clip.wav](assets/audio/content/content-l5-real-dialogue-emotion/clip.wav) · 15.42s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** Two women discuss a past belief and one of them being asked out by a guy named Chip Matthews.
- **Why the answer stands** The report explicitly states that Speaker 1 sounds 'excited and surprised' and Speaker 2 sounds 'mildly surprised or amused', which directly supports the claimed answer of both sounding surprised.
- **Difficulty** score 0.7043 (auditor answered 0/5 blind, training solver 0.3333333333333333)

### `content-l5-dialogue-emotion`

- **Question** Which speaker sounds happy?
- **Answer** D. the man
- **Audio** [assets/audio/content/content-l5-dialogue-emotion/clip.wav](assets/audio/content/content-l5-dialogue-emotion/clip.wav) · 25.89s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man and a woman take turns reading short, unrelated sentences in Chinese with contrasting neutral and cheerful tones.
- **Why the answer stands** The report states that Speaker 2 (the man) speaks with a cheerful, warm, and positive tone, while Speaker 1 (the woman) speaks in a calm, slightly weary, and neutral tone.
- **Difficulty** score 0.4856 (auditor answered 5/5 blind, training solver 0.0)


## Multi-clip & Long Scene — L1

### `multi-l1-long-scene-real`

- **Question** What sound comes immediately after the speech?
- **Answer** C. accordion
- **Audio** [assets/audio/multi/multi-l1-long-scene-real/clip.wav](assets/audio/multi/multi-l1-long-scene-real/clip.wav) · 50.02s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The recording features background hiss, a thud, a dog barking, a man speaking, a short accordion note, and a final dog bark.
- **Why the answer stands** The report states that the man speaks at 0:06 and the next sound heard is an accordion note at 0:18, which directly supports the claimed answer.
- **Difficulty** score 0.1762 (auditor answered 5/5 blind, training solver 0.75)

### `multi-l1-long-scene`

- **Question** Over the whole recording, how many times does the jingle bell sound occur?
- **Answer** D. 2
- **Audio** [assets/audio/multi/multi-l1-long-scene/clip.wav](assets/audio/multi/multi-l1-long-scene/clip.wav) · 25.35s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two clips sharing a background appliance hum and metallic clink, with the first clip ending in a sneeze and the second ending in a rooster crow.
- **Why the answer stands** The report describes a 'metallic clinking' sound occurring twice (at 1.0s and 5.0s), which corresponds to the 'jingle bell sound' in the question occurring 2 times.
- **Difficulty** score 0.1773 (auditor answered 5/5 blind, training solver 0.6666666666666666)

### `multi-l1-multi-contains`

- **Question** Which clip contains the sound of scream?
- **Answer** B. the first clip
- **Audio** [assets/audio/multi/multi-l1-multi-contains/clip1.wav](assets/audio/multi/multi-l1-multi-contains/clip1.wav) (+2 more clips) · 9.74s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The recording consists of three short clips: a loud human scream, followed by a low-pitched electronic buzz, and ending with a higher-pitched electronic buzz.
- **Why the answer stands** The report explicitly states that Clip 1 contains a loud, high-pitched human scream, which directly supports the claimed answer B.
- **Difficulty** score 0.1817 (auditor answered 5/5 blind, training solver 0.75)

### `multi-l1-multi-audio`

- **Question** You hear two separate audio clips. Which of them contains a burping sound?
- **Answer** A. both clips
- **Audio** [assets/audio/multi/multi-l1-multi-audio/clip1.wav](assets/audio/multi/multi-l1-multi-audio/clip1.wav) (+1 more clips) · 11.32s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two clips featuring belching sounds, separated by a notification chime, with the second clip ending in a resonant ringing tone.
- **Why the answer stands** The report explicitly states that Clip 1 contains wet belches, Clip 2 contains a short belch, and both clips share the sound of human belching (burping).
- **Difficulty** score 0.1711 (auditor answered 5/5 blind, training solver 0.6666666666666666)

### `multi-l1-multi-same-speaker`

- **Question** Do both clips feature the same speaker?
- **Answer** A. Yes, the same speaker
- **Audio** [assets/audio/multi/multi-l1-multi-same-speaker/clip1.wav](assets/audio/multi/multi-l1-multi-same-speaker/clip1.wav) (+1 more clips) · 8.12s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains two short clips of a female speaker delivering historical speeches, with the second clip ending in audience applause.
- **Why the answer stands** The report explicitly states that both clips feature one distinct speaker who sounds very similar or identical, which supports the claimed answer.
- **Difficulty** score 0.1978 (auditor answered 4/5 blind, training solver 0.75)

### `multi-l1-multi-clip-crossref`

- **Question** Which clip contains the same sound source as clip 1?
- **Answer** B. clip 2
- **Audio** [assets/audio/multi/multi-l1-multi-clip-crossref/clip1.wav](assets/audio/multi/multi-l1-multi-clip-crossref/clip1.wav) (+2 more clips) · 5.8s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two consecutive human burps followed by the sound of a drawer sliding shut.
- **Why the answer stands** The report explicitly states that Clips 1 and 2 share the same sound of a burp, which directly supports option B.
- **Difficulty** score 0.1287 (auditor answered 5/5 blind, training solver 0.75)


## Multi-clip & Long Scene — L2

### `multi-l2-long-scene-real`

- **Question** Immediately following the spoken voice, which sound occurs?
- **Answer** B. crumpling paper
- **Audio** [assets/audio/multi/multi-l2-long-scene-real/clip.wav](assets/audio/multi/multi-l2-long-scene-real/clip.wav) · 34.31s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a series of sound effects, including creaking, splashing, crinkling, and clicking, interspersed with a woman asking, 'What true things are told in stories?'
- **Why the answer stands** The report states that 'plastic or paper crinkling' occurs at 6.0s, immediately following the woman speaking at 4.0s, which matches the claimed answer of 'crumpling paper'.
- **Difficulty** score 0.2441 (auditor answered 5/5 blind, training solver 0.75)

### `multi-l2-multi-contains`

- **Question** In which clip can you hear the sound of giggle?
- **Answer** D. the third clip
- **Audio** [assets/audio/multi/multi-l2-multi-contains/clip1.wav](assets/audio/multi/multi-l2-multi-contains/clip1.wav) (+2 more clips) · 15.0s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The recording consists of three distinct clips: a rapid clicking sound, an electronic beep with a low rumble, and a man laughing followed by a groan.
- **Why the answer stands** The report states that Clip 3 contains a man laughing, which supports the claimed answer that a giggle can be heard in the third clip.
- **Difficulty** score 0.2616 (auditor answered 5/5 blind, training solver 0.75)

### `multi-l2-multi-clip-crossref`

- **Question** Which clip contains speech?
- **Answer** D. clip 2
- **Audio** [assets/audio/multi/multi-l2-multi-clip-crossref/clip1.wav](assets/audio/multi/multi-l2-multi-clip-crossref/clip1.wav) (+1 more clips) · 6.61s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The recording features the sound of footsteps walking on wood, followed by a female voice saying 'His cousin was a very brilliant girl' amidst a cheering crowd.
- **Why the answer stands** The report explicitly states that Clip 1 contains no speakers, while Clip 2 contains a female speaker, which directly supports the claimed answer that Clip 2 contains speech.
- **Difficulty** score 0.2558 (auditor answered 5/5 blind, training solver 0.5)

### `multi-l2-multi-compare-attr`

- **Question** Which clip has the greater number of distinct speakers?
- **Answer** B. the second clip
- **Audio** [assets/audio/multi/multi-l2-multi-compare-attr/clip1.wav](assets/audio/multi/multi-l2-multi-compare-attr/clip1.wav) (+1 more clips) · 9.52s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two clips: the first features two speakers discussing an illness and hay fever, while the second features a female speaker, whispered dialogue, and background insect buzzing.
- **Why the answer stands** The report explicitly states that Clip 1 contains 2 distinct speakers and Clip 2 contains 3 distinct speakers, which supports the claim that the second clip has the greater number of distinct speakers.
- **Difficulty** score 0.3035 (auditor answered 5/5 blind, training solver 0.75)

### `multi-l2-multi-same-speaker`

- **Question** Are the two clips spoken by the same person?
- **Answer** D. No, two different speakers
- **Audio** [assets/audio/multi/multi-l2-multi-same-speaker/clip1.wav](assets/audio/multi/multi-l2-multi-same-speaker/clip1.wav) (+1 more clips) · 7.2s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains two separate clips of spoken English: first, a male voice reading a sentence, followed by a female voice reading a different sentence.
- **Why the answer stands** The report explicitly states that Clip 1 features a male speaker and Clip 2 features a female speaker, confirming that there are two different speakers.
- **Difficulty** score 0.2386 (auditor answered 5/5 blind, training solver 0.5)

### `multi-l2-multi-audio`

- **Question** You hear two separate audio clips. Which of them contains a coin (dropping) sound?
- **Answer** A. both clips
- **Audio** [assets/audio/multi/multi-l2-multi-audio/clip1.wav](assets/audio/multi/multi-l2-multi-audio/clip1.wav) (+1 more clips) · 9.34s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two clips featuring metallic rattling sounds, with the second clip ending with a child's laugh.
- **Why the answer stands** The report explicitly states that both Clip 1 and Clip 2 contain a metallic rattling sound described as being like coins or keys shaking.
- **Difficulty** score 0.2463 (auditor answered 5/5 blind, training solver 0.5)


## Multi-clip & Long Scene — L3

### `multi-l3-long-scene-real`

- **Question** Which sound occurs last in the recording?
- **Answer** D. tearing
- **Audio** [assets/audio/multi/multi-l3-long-scene-real/clip.wav](assets/audio/multi/multi-l3-long-scene-real/clip.wav) · 53.66s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A single recording features continuous insect buzzing, rustling noises, a sniff, a female speaker, and a sneeze.
- **Why the answer stands** The report states that a rustling sound is the final event at 28.0s, which supports the option of 'tearing' as the last sound.
- **Difficulty** score 0.3335 (auditor answered 5/5 blind, training solver 0.5)

### `multi-l3-long-scene`

- **Question** Apart from the continuous background, which distinct sound event occurs first?
- **Answer** B. Crushing
- **Audio** [assets/audio/multi/multi-l3-long-scene/clip.wav](assets/audio/multi/multi-l3-long-scene/clip.wav) · 20.35s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains the sound of a person snoring, interspersed with plastic cracking noises and a short phone vibration near the end.
- **Why the answer stands** The report identifies a 'plastic cracking sound' at 1.1s as the first event after the background snoring, which corresponds to the 'Crushing' option.
- **Difficulty** score 0.4023 (auditor answered 2/5 blind, training solver 0.6666666666666666)

### `multi-l3-multi-contains`

- **Question** In which clip can you hear the sound of giggle?
- **Answer** B. the third clip
- **Audio** [assets/audio/multi/multi-l3-multi-contains/clip1.wav](assets/audio/multi/multi-l3-multi-contains/clip1.wav) (+2 more clips) · 13.54s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The recording consists of three clips: a buzzing hair clipper, a gasp followed by the buzzing, and a man and woman laughing heartily.
- **Why the answer stands** The report states that the third clip contains a man and a woman laughing, which supports the answer that a giggle (a type of laugh) can be heard in the third clip.
- **Difficulty** score 0.4018 (auditor answered 5/5 blind, training solver 0.0)

### `multi-l3-multi-clip-crossref`

- **Question** In which clip can you hear someone talking?
- **Answer** B. clip 2
- **Audio** [assets/audio/multi/multi-l3-multi-clip-crossref/clip1.wav](assets/audio/multi/multi-l3-multi-clip-crossref/clip1.wav) (+2 more clips) · 15.4s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of three distinct clips: a harmonica melody, a man speaking, and a revving engine.
- **Why the answer stands** The report explicitly states that Clip 2 contains a single male speaker, while Clip 1 and Clip 3 contain no speakers.
- **Difficulty** score 0.3273 (auditor answered 5/5 blind, training solver 0.75)

### `multi-l3-multi-compare-attr`

- **Question** Which clip has the greater number of distinct speakers?
- **Answer** B. the first clip
- **Audio** [assets/audio/multi/multi-l3-multi-compare-attr/clip1.wav](assets/audio/multi/multi-l3-multi-compare-attr/clip1.wav) (+1 more clips) · 9.25s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains two clips: the first has two female voices separated by a chime, and the second features a male voice speaking.
- **Why the answer stands** The report explicitly states that Clip 1 has two distinct speakers while Clip 2 has one, which directly supports the claimed answer that the first clip has the greater number of distinct speakers.
- **Difficulty** score 0.389 (auditor answered 2/5 blind, training solver 0.75)

### `multi-l3-multi-same-speaker`

- **Question** Were these two clips recorded by the same speaker?
- **Answer** B. No, two different speakers
- **Audio** [assets/audio/multi/multi-l3-multi-same-speaker/clip1.wav](assets/audio/multi/multi-l3-multi-same-speaker/clip1.wav) (+1 more clips) · 8.1s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains a short clip of a man speaking, followed immediately by a longer clip of a woman speaking.
- **Why the answer stands** The report explicitly states that Clip 1 features a male speaker and Clip 2 features a female speaker, confirming that there are two different speakers.
- **Difficulty** score 0.3574 (auditor answered 5/5 blind, training solver 0.0)


## Multi-clip & Long Scene — L4

### `multi-l4-long-scene-real`

- **Question** What is the final sound event in this long recording?
- **Answer** B. crack
- **Audio** [assets/audio/multi/multi-l4-long-scene-real/clip.wav](assets/audio/multi/multi-l4-long-scene-real/clip.wav) · 37.05s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains two clips featuring background car traffic, plastic clicks, claps, a bird chirping, and a man speaking about an experiment.
- **Why the answer stands** The report identifies the final event as a 'loud clap', which is a close match/paraphrase for a 'crack' sound, and none of the other options fit this description.
- **Difficulty** score 0.498 (auditor answered 4/5 blind, training solver 0.0)

### `multi-l4-multi-contains`

- **Question** In which clip can you hear the sound of sigh?
- **Answer** D. the second clip
- **Audio** [assets/audio/multi/multi-l4-multi-contains/clip1.wav](assets/audio/multi/multi-l4-multi-contains/clip1.wav) (+1 more clips) · 10.49s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two clips: the first featuring a low synthesizer note and plastic rustling, and the second featuring plastic rustling and a deep exhale.
- **Why the answer stands** The report states that Clip 2 contains a deep, heavy exhale (which corresponds to a sigh), while Clip 1 does not.
- **Difficulty** score 0.4739 (auditor answered 3/5 blind, training solver 0.5)

### `multi-l4-long-scene`

- **Question** Over the whole recording, how many times does the crushing sound occur?
- **Answer** A. 2
- **Audio** [assets/audio/multi/multi-l4-long-scene/clip.wav](assets/audio/multi/multi-l4-long-scene/clip.wav) · 20.35s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains two clips of plastic rustling, with the first clip also featuring a car horn honk.
- **Why the answer stands** The report describes two instances of plastic rustling, which corresponds to the crushing sound occurring twice.
- **Difficulty** score 0.4793 (auditor answered 3/5 blind, training solver 0.3333333333333333)

### `multi-l4-multi-compare-attr`

- **Question** Which clip contains more speakers?
- **Answer** B. the second clip
- **Audio** [assets/audio/multi/multi-l4-multi-compare-attr/clip1.wav](assets/audio/multi/multi-l4-multi-compare-attr/clip1.wav) (+1 more clips) · 13.45s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two clips containing spoken English passages, with the first clip featuring a single female speaker and the second clip featuring three different speakers reading literary fragments.
- **Why the answer stands** The report explicitly states that Clip 1 has 1 speaker while Clip 2 has 3 speakers, which directly supports the claimed answer that the second clip contains more speakers.
- **Difficulty** score 0.4765 (auditor answered 4/5 blind, training solver 0.0)

### `multi-l4-multi-same-speaker`

- **Question** Were these two clips recorded by the same speaker?
- **Answer** A. Yes, the same speaker
- **Audio** [assets/audio/multi/multi-l4-multi-same-speaker/clip1.wav](assets/audio/multi/multi-l4-multi-same-speaker/clip1.wav) (+1 more clips) · 8.32s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two separate clips of a female speaker with a British accent reading different sentences.
- **Why the answer stands** The report explicitly states that both clips share a female speaker, which directly supports the claimed answer.
- **Difficulty** score 0.4538 (auditor answered 3/5 blind, training solver 0.25)

### `multi-l4-multi-clip-crossref`

- **Question** Which clip contains the same sound source as clip 1?
- **Answer** C. clip 2
- **Audio** [assets/audio/multi/multi-l4-multi-clip-crossref/clip1.wav](assets/audio/multi/multi-l4-multi-clip-crossref/clip1.wav) (+2 more clips) · 9.01s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The recording contains three clips in sequence: rapid light knocking, heavy slow knocking, and a single resonant chime.
- **Why the answer stands** The report explicitly states that Clips 1 and 2 share the sound of knocking on wood, which supports the claimed answer that Clip 2 contains the same sound source as Clip 1.
- **Difficulty** score 0.4148 (auditor answered 5/5 blind, training solver 0.25)


## Multi-clip & Long Scene — L5

### `multi-l5-long-scene-real`

- **Question** What sound comes immediately after the speech?
- **Answer** A. shuffling cards
- **Audio** [assets/audio/multi/multi-l5-long-scene-real/clip.wav](assets/audio/multi/multi-l5-long-scene-real/clip.wav) · 34.7s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A rhythmic hand clapping sequence is interspersed with a synthesizer drone, a cymbal crash, a chime, a spoken sentence, and a scratching sound.
- **Why the answer stands** The report states that a scratching sound occurs at 12.1s immediately after the man speaks at 8.0s, which matches the option of shuffling cards.
- **Difficulty** score 0.6302 (auditor answered 5/5 blind, training solver 0.0)

### `multi-l5-multi-contains`

- **Question** Which of the clips includes footsteps sounds?
- **Answer** A. the first clip
- **Audio** [assets/audio/multi/multi-l5-multi-contains/clip1.wav](assets/audio/multi/multi-l5-multi-contains/clip1.wav) (+2 more clips) · 13.94s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of three distinct clips featuring footsteps walking, paper or plastic crinkling, and a door opening and closing.
- **Why the answer stands** The report explicitly states that Clip 1 contains the sound of footsteps walking on a hard floor, which directly supports option A.
- **Difficulty** score 0.518 (auditor answered 5/5 blind, training solver 0.0)

### `multi-l5-multi-same-speaker`

- **Question** Are the two clips spoken by the same person?
- **Answer** C. No, two different speakers
- **Audio** [assets/audio/multi/multi-l5-multi-same-speaker/clip1.wav](assets/audio/multi/multi-l5-multi-same-speaker/clip1.wav) (+1 more clips) · 5.14s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two clips: first, a man asking about logical evidence over quiet traffic, followed by a woman stating that something is quite true over louder traffic noise.
- **Why the answer stands** The report explicitly states that Clip 1 contains a single male speaker and Clip 2 contains a single female speaker, confirming there are two different speakers.
- **Difficulty** score 0.5537 (auditor answered 5/5 blind, training solver 0.0)

### `multi-l5-multi-audio`

- **Question** You hear two separate audio clips. Which of them contains a coin (dropping) sound?
- **Answer** A. both clips
- **Audio** [assets/audio/multi/multi-l5-multi-audio/clip1.wav](assets/audio/multi/multi-l5-multi-audio/clip1.wav) (+1 more clips) · 12.35s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two clips, both starting with a spinning coin sound, followed by a rooster crowing in the first clip and a man sneezing in the second.
- **Why the answer stands** The report explicitly states that both clips start with a spinning coin sound, which supports the claimed answer that both clips contain a coin sound.
- **Difficulty** score 0.5557 (auditor answered 4/5 blind, training solver 0.0)

### `multi-l5-multi-compare-attr`

- **Question** Which of the two clips features more voices?
- **Answer** A. the second clip
- **Audio** [assets/audio/multi/multi-l5-multi-compare-attr/clip1.wav](assets/audio/multi/multi-l5-multi-compare-attr/clip1.wav) (+1 more clips) · 13.43s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two clips containing spoken English literary passages, featuring a female speaker in the first clip, and a male followed by a female speaker in the second clip.
- **Why the answer stands** The report explicitly states that Clip 1 contains a single female speaker, while Clip 2 contains two distinct speakers, which supports the claimed answer that the second clip features more voices.
- **Difficulty** score 0.5511 (auditor answered 0/5 blind, training solver 0.5)

### `multi-l5-multi-contains-2`

- **Question** Which of the clips includes finger snap sounds?
- **Answer** B. the third clip
- **Audio** [assets/audio/multi/multi-l5-multi-contains-2/clip1.wav](assets/audio/multi/multi-l5-multi-contains-2/clip1.wav) (+2 more clips) · 9.29s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The recording consists of three clips sharing a background of flowing water, featuring a chime in the first, a female Chinese voice in the second, and a finger snap in the third.
- **Why the answer stands** The report explicitly states that Clip 3 contains a finger snap, which directly supports the claimed answer B.
- **Difficulty** score 0.5096 (auditor answered 4/5 blind, training solver 0.5)


## Music — L1

### `music-l1-music-segment-louder`

- **Question** Of the two music segments, which one is louder?
- **Answer** C. the first segment
- **Audio** [assets/audio/music/music-l1-music-segment-louder/clip.wav](assets/audio/music/music-l1-music-segment-louder/clip.wav) · 9.02s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains an upbeat electronic music cue with children cheering, followed by a descending synthesizer chord and a crowd groaning.
- **Why the answer stands** The report explicitly states that the first part is louder than the second part, which supports the claimed answer.
- **Difficulty** score 0.2009 (auditor answered 5/5 blind, training solver 0.5)

### `music-l1-music-genre-real`

- **Question** What is the genre of this music?
- **Answer** A. ambient
- **Audio** [assets/audio/music/music-l1-music-genre-real/clip.wav](assets/audio/music/music-l1-music-genre-real/clip.wav) · 10.4s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short, peaceful ambient track featuring a slow synthesizer pad and two resonant chime strikes.
- **Why the answer stands** The report explicitly states that the genre of the music is ambient or New Age meditation music.
- **Difficulty** score 0.154 (auditor answered 5/5 blind, training solver 1.0)

### `music-l1-music-pitch-shift-compare`

- **Question** Compared with the first excerpt, the second one is …
- **Answer** D. lower in pitch
- **Audio** [assets/audio/music/music-l1-music-pitch-shift-compare/clip.wav](assets/audio/music/music-l1-music-pitch-shift-compare/clip.wav) · 10.04s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains two synthesizer chords separated and followed by vinyl scratch sound effects.
- **Why the answer stands** The report explicitly states that the second synthesizer chord is lower-pitched than the first one.
- **Difficulty** score 0.2213 (auditor answered 5/5 blind, training solver 0.75)

### `music-l1-music-tempo-change`

- **Question** Does the music speed up, slow down or keep its tempo in the second half?
- **Answer** C. The second half is slower
- **Audio** [assets/audio/music/music-l1-music-tempo-change/clip.wav](assets/audio/music/music-l1-music-tempo-change/clip.wav) · 12.19s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio transitions from a fast, energetic solo piano jazz intro to a slow, smooth jazz ensemble piece featuring saxophone, double bass, and drums.
- **Why the answer stands** The report explicitly states that the tempo abruptly slows down to a slow, steady pace in the second part, which directly supports the claimed answer.
- **Difficulty** score 0.131 (auditor answered 5/5 blind, training solver 0.75)

### `music-l1-music-dynamics-real`

- **Question** How does the volume of the music change from beginning to end?
- **Answer** B. it gradually gets louder (crescendo)
- **Audio** [assets/audio/music/music-l1-music-dynamics-real/clip.wav](assets/audio/music/music-l1-music-dynamics-real/clip.wav) · 8.74s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a rising synthesizer swell followed by a series of powerful, rhythmic orchestral drum strikes.
- **Why the answer stands** The report states that the beginning of the synthesizer swell is the quietest and the subsequent drum hits are the loudest, which supports the claim that the music gradually gets louder (crescendo).
- **Difficulty** score 0.2392 (auditor answered 5/5 blind, training solver 0.5)

### `music-l1-song-in-scene`

- **Question** What sound occurs on top of the music?
- **Answer** B. Baby laughter
- **Audio** [assets/audio/music/music-l1-song-in-scene/clip.wav](assets/audio/music/music-l1-song-in-scene/clip.wav) · 10.56s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short ambient synthesizer melody plays, accompanied by a child's giggle halfway through.
- **Why the answer stands** The report explicitly mentions 'a child giggling' occurring during the music, which directly supports the claimed answer of 'Baby laughter'.
- **Difficulty** score 0.0833 (auditor answered 5/5 blind, training solver 0.8333333333333334)


## Music — L2

### `music-l2-music-segment-louder`

- **Question** Compare the two segments: which is louder?
- **Answer** A. the second segment
- **Audio** [assets/audio/music/music-l2-music-segment-louder/clip.wav](assets/audio/music/music-l2-music-segment-louder/clip.wav) · 8.66s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short, upbeat electronic music cue featuring synthesizers and a drum beat.
- **Why the answer stands** The report states that the loudest part is between 2 and 4 seconds when all elements are playing, which supports the claim that the second segment is louder than the first.
- **Difficulty** score 0.304 (auditor answered 2/5 blind, training solver 0.75)

### `music-l2-music-vocals-present`

- **Question** What kind of vocals are in this recording?
- **Answer** D. a choir
- **Audio** [assets/audio/music/music-l2-music-vocals-present/clip.wav](assets/audio/music/music-l2-music-vocals-present/clip.wav) · 10.4s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a brief ambient introduction with a synthesizer sweep followed by a male choir singing a sustained 'Amen' chord.
- **Why the answer stands** The report repeatedly and explicitly mentions a male choir singing, which directly supports the claimed answer of 'a choir'.
- **Difficulty** score 0.2924 (auditor answered 5/5 blind, training solver 0.75)

### `music-l2-music-pitch-shift-compare`

- **Question** How does the pitch of the second excerpt compare with the first?
- **Answer** C. lower in pitch
- **Audio** [assets/audio/music/music-l2-music-pitch-shift-compare/clip.wav](assets/audio/music/music-l2-music-pitch-shift-compare/clip.wav) · 10.84s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short, six-second instrumental clip featuring a brass ensemble playing a bright chord progression followed by a lower, darker one.
- **Why the answer stands** The report explicitly states that the pitch is lower in the second half of the clip compared to the first.
- **Difficulty** score 0.2794 (auditor answered 5/5 blind, training solver 0.5)

### `music-l2-music-tempo-change`

- **Question** Does the music speed up, slow down or keep its tempo in the second half?
- **Answer** C. The second half is slower
- **Audio** [assets/audio/music/music-l2-music-tempo-change/clip.wav](assets/audio/music/music-l2-music-tempo-change/clip.wav) · 11.17s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a transition from an upbeat acoustic guitar melody to a slower, atmospheric synthesizer tune.
- **Why the answer stands** The report explicitly states that the tempo abruptly slows down in the second half and describes the second half as a slower tune.
- **Difficulty** score 0.2796 (auditor answered 5/5 blind, training solver 0.5)

### `music-l2-music-speed-compare`

- **Question** How does the speed of the second excerpt compare with the first?
- **Answer** A. slower
- **Audio** [assets/audio/music/music-l2-music-speed-compare/clip.wav](assets/audio/music/music-l2-music-speed-compare/clip.wav) · 11.99s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An upbeat electronic video game track featuring a fast synth intro followed by a steady, groovy synth and drum loop.
- **Why the answer stands** The report states that the music starts with a fast-tempo intro and then transitions to a moderate-tempo beat, which supports the claim that the second part is slower.
- **Difficulty** score 0.2864 (auditor answered 5/5 blind, training solver 0.25)

### `music-l2-music-dynamics-real`

- **Question** How does the loudness evolve over the clip?
- **Answer** A. it stays about the same
- **Audio** [assets/audio/music/music-l2-music-dynamics-real/clip.wav](assets/audio/music/music-l2-music-dynamics-real/clip.wav) · 8.8s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short loop of electronic music featuring a synth bassline and a steady percussive beat.
- **Why the answer stands** The report explicitly states that 'The volume is constant throughout the clip', which directly supports the claimed answer that the loudness stays about the same.
- **Difficulty** score 0.3078 (auditor answered 4/5 blind, training solver 0.75)


## Music — L3

### `music-l3-music-vocals-present`

- **Question** Which description of the vocals fits this excerpt?
- **Answer** B. a choir
- **Audio** [assets/audio/music/music-l3-music-vocals-present/clip.wav](assets/audio/music/music-l3-music-vocals-present/clip.wav) · 10.4s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An a cappella choir sings a slow, harmonious 'Amen' cadence.
- **Why the answer stands** The report explicitly and repeatedly mentions a choir singing, which directly supports option B.
- **Difficulty** score 0.3241 (auditor answered 5/5 blind, training solver 0.75)

### `music-l3-song-change`

- **Question** How does the music change during this clip?
- **Answer** A. the genre changes from heavy metal to classical
- **Audio** [assets/audio/music/music-l3-song-change/clip.wav](assets/audio/music/music-l3-song-change/clip.wav) · 26.85s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a sudden transition from an energetic rock song with male vocals to a dramatic, ambient operatic piece with female vocalizations.
- **Why the answer stands** The report describes a transition from upbeat rock/J-Rock to operatic music, which corresponds to the transition from heavy metal to classical in the claimed answer.
- **Difficulty** score 0.3329 (auditor answered 5/5 blind, training solver 0.3333333333333333)

### `music-l3-music-pitch-shift-compare`

- **Question** Compared with the first excerpt, the second one is …
- **Answer** A. lower in pitch
- **Audio** [assets/audio/music/music-l3-music-pitch-shift-compare/clip.wav](assets/audio/music/music-l3-music-pitch-shift-compare/clip.wav) · 9.84s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a short electronic synthesizer piece featuring an ascending arpeggio followed by a descending arpeggio.
- **Why the answer stands** The report explicitly states that the pitch is lower in the second part compared to the first part.
- **Difficulty** score 0.3786 (auditor answered 5/5 blind, training solver 0.25)

### `music-l3-music-segment-louder`

- **Question** Of the two music segments, which one is louder?
- **Answer** C. the first segment
- **Audio** [assets/audio/music/music-l3-music-segment-louder/clip.wav](assets/audio/music/music-l3-music-segment-louder/clip.wav) · 8.1s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio transitions abruptly from an upbeat electronic dance song with female vocals to a slower swing jazz song with male vocals.
- **Why the answer stands** The report states the first segment is compressed and consistently loud, while the second has dynamic variation, which supports the first segment being louder overall.
- **Difficulty** score 0.3844 (auditor answered 2/5 blind, training solver 0.75)

### `music-l3-music-tempo-change`

- **Question** Compared with the first half, how does the tempo of the second half change?
- **Answer** C. The second half is slower
- **Audio** [assets/audio/music/music-l3-music-tempo-change/clip.wav](assets/audio/music/music-l3-music-tempo-change/clip.wav) · 11.72s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio captures a transition from a live rock performance with electric guitar and crowd cheering to a synthesizer-driven electronic track.
- **Why the answer stands** The report explicitly states that the tempo shifts from around 125 BPM in the first part to a slightly slower tempo of about 115 BPM in the second part.
- **Difficulty** score 0.3389 (auditor answered 5/5 blind, training solver 0.25)

### `music-l3-music-dynamics-real`

- **Question** Which description of the dynamics fits this excerpt?
- **Answer** B. it stays about the same
- **Audio** [assets/audio/music/music-l3-music-dynamics-real/clip.wav](assets/audio/music/music-l3-music-dynamics-real/clip.wav) · 9.5s · 4 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short, 5-second upbeat indie pop instrumental track featuring acoustic guitar, drums, bass, and a synth melody.
- **Why the answer stands** The report explicitly states that 'The loudness is uniform from start to finish', which directly supports the claimed answer that the dynamics stay about the same.
- **Difficulty** score 0.3093 (auditor answered 5/5 blind, training solver 0.25)


## Music — L4

### `music-l4-song-change`

- **Question** Roughly how many seconds into the clip does the music change?
- **Answer** D. about 9 seconds
- **Audio** [assets/audio/music/music-l4-song-change/clip.wav](assets/audio/music/music-l4-song-change/clip.wav) · 20.33s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features two distinct musical clips: a fast-paced rock song followed by a slower acoustic indie song, both with male vocals.
- **Why the answer stands** The report states that there is an abrupt cut to a different song at 8.0 seconds, which closely aligns with the claimed answer of 'about 9 seconds' (Option D).
- **Difficulty** score 0.4023 (auditor answered 4/5 blind, training solver 0.3333333333333333)

### `music-l4-music-segment-louder`

- **Question** Which of the two passages is played at the higher volume?
- **Answer** A. the first segment
- **Audio** [assets/audio/music/music-l4-music-segment-louder/clip.wav](assets/audio/music/music-l4-music-segment-louder/clip.wav) · 9.81s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a fast electronic dance beat that abruptly transitions into a slow, ambient section featuring a female operatic vocal.
- **Why the answer stands** The report explicitly states that the first part is played loudest, which directly supports the claimed answer that the first segment is played at the higher volume.
- **Difficulty** score 0.4236 (auditor answered 5/5 blind, training solver 0.25)

### `music-l4-music-dynamics-real`

- **Question** Over the course of the recording, what happens to the loudness?
- **Answer** C. it stays about the same
- **Audio** [assets/audio/music/music-l4-music-dynamics-real/clip.wav](assets/audio/music/music-l4-music-dynamics-real/clip.wav) · 8.74s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short, repeating electronic music loop featuring a synth bassline and a drum machine beat.
- **Why the answer stands** The report explicitly states that 'The loudness is uniform throughout the clip', which directly supports the claimed answer that it stays about the same.
- **Difficulty** score 0.4261 (auditor answered 4/5 blind, training solver 0.5)

### `music-l4-music-pitch-shift-compare`

- **Question** Compared with the first excerpt, the second one is …
- **Answer** A. lower in pitch
- **Audio** [assets/audio/music/music-l4-music-pitch-shift-compare/clip.wav](assets/audio/music/music-l4-music-pitch-shift-compare/clip.wav) · 9.9s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short audio clip featuring a fast, lively melody played on an accordion in two similar phrases.
- **Why the answer stands** The report states that the second phrase starts slightly lower than the peak of the first and has melodic variations, while the tempo remains constant, which supports the claim that it is lower in pitch.
- **Difficulty** score 0.4687 (auditor answered 5/5 blind, training solver 0.25)

### `music-l4-music-instrument-present`

- **Question** What is the main instrument you hear?
- **Answer** D. clarinet
- **Audio** [assets/audio/music/music-l4-music-instrument-present/clip.wav](assets/audio/music/music-l4-music-instrument-present/clip.wav) · 10.4s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short, cheerful Dixieland jazz instrumental featuring brass, woodwinds, banjo, and percussion.
- **Why the answer stands** The report explicitly lists the clarinet as one of the instruments present in the excerpt, while none of the other options (saxophone, marimba, bagpipes) are mentioned.
- **Difficulty** score 0.3899 (auditor answered 4/5 blind, training solver 0.75)

### `music-l4-music-tempo-change`

- **Question** How does the tempo of the second half compare with the first half?
- **Answer** A. Both halves have the same tempo
- **Audio** [assets/audio/music/music-l4-music-tempo-change/clip.wav](assets/audio/music/music-l4-music-tempo-change/clip.wav) · 9.75s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An upbeat electronic dance music track plays briefly, featuring a vocal shout of 'Let's go!' and a record scratch effect.
- **Why the answer stands** The report explicitly states that the tempo stays constant at around 128 BPM, which supports the claim that both halves have the same tempo.
- **Difficulty** score 0.4345 (auditor answered 2/5 blind, training solver 0.25)


## Music — L5

### `music-l5-music-segment-louder`

- **Question** Which of the two passages is played at the higher volume?
- **Answer** B. the second segment
- **Audio** [assets/audio/music/music-l5-music-segment-louder/clip.wav](assets/audio/music/music-l5-music-segment-louder/clip.wav) · 7.69s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a slide whistle sliding up and down in pitch, ending with a sharp cymbal and drum crash.
- **Why the answer stands** The report states that the loudest part of the audio is the drum and cymbal crash at the end (the second segment), while the slide whistle (the first segment) is quieter, which directly supports option B.
- **Difficulty** score 0.6124 (auditor answered 2/5 blind, training solver 0.25)

### `music-l5-music-dynamics-real`

- **Question** How does the volume of the music change from beginning to end?
- **Answer** B. it stays about the same
- **Audio** [assets/audio/music/music-l5-music-dynamics-real/clip.wav](assets/audio/music/music-l5-music-dynamics-real/clip.wav) · 9.5s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features the sound of a typewriter typing accompanied by a soft, minimalist ambient synthesizer melody.
- **Why the answer stands** The report explicitly states that 'the loudness is consistent, with a gentle fade-out at the very end,' which supports the claimed answer that the volume stays about the same.
- **Difficulty** score 0.6559 (auditor answered 0/5 blind, training solver 0.0)

### `music-l5-music-speed-compare`

- **Question** Compared with the first excerpt, the second one is played …
- **Answer** A. the same speed
- **Audio** [assets/audio/music/music-l5-music-speed-compare/clip.wav](assets/audio/music/music-l5-music-speed-compare/clip.wav) · 10.62s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a short, repeating electronic dance music loop featuring synthesizers and electronic drums.
- **Why the answer stands** The report states that the tempo is constant at around 120 BPM throughout the repeating loop, which supports the claim that the second excerpt is played at the same speed.
- **Difficulty** score 0.6019 (auditor answered 0/5 blind, training solver 0.25)

### `music-l5-music-tempo-change`

- **Question** Does the music speed up, slow down or keep its tempo in the second half?
- **Answer** D. Both halves have the same tempo
- **Audio** [assets/audio/music/music-l5-music-tempo-change/clip.wav](assets/audio/music/music-l5-music-tempo-change/clip.wav) · 9.75s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A short, fast-paced clip of electronic J-pop music featuring high-pitched Vocaloid singing.
- **Why the answer stands** The report explicitly states that the tempo remains constant throughout the clip, which directly supports the claimed answer that both halves have the same tempo.
- **Difficulty** score 0.5095 (auditor answered 2/5 blind, training solver 0.0)

### `music-l5-music-pitch`

- **Question** Two instruments play one after the other. Which one plays the higher notes?
- **Answer** D. marimba
- **Audio** [assets/audio/music/music-l5-music-pitch/clip.wav](assets/audio/music/music-l5-music-pitch/clip.wav) · 8.58s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a synthesizer melody, a single woodblock strike, and a short marimba scale.
- **Why the answer stands** The report explicitly states that the pitch is higher in the second part, which is played by the marimba.
- **Difficulty** score 0.7734 (auditor answered 1/5 blind, training solver 0.0)

### `music-l5-song-in-scene`

- **Question** What sound occurs on top of the music?
- **Answer** C. Dishes, pots, and pans
- **Audio** [assets/audio/music/music-l5-song-in-scene/clip.wav](assets/audio/music/music-l5-song-in-scene/clip.wav) · 14.75s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An upbeat electronic music track plays briefly, accompanied by a couple of sharp clicks and a metallic clink.
- **Why the answer stands** The report mentions a 'metallic clinking sound' which supports the claimed answer of 'Dishes, pots, and pans'.
- **Difficulty** score 0.7805 (auditor answered 0/5 blind, training solver 0.16666666666666666)


## Speech Prosody — L1

### `prosody-l1-speed-pattern3`

- **Question** Listen to the three utterances. What is the speaking-speed pattern (from the first to the third)?
- **Answer** B. high-low-medium
- **Audio** [assets/audio/prosody/prosody-l1-speed-pattern3/clip.wav](assets/audio/prosody/prosody-l1-speed-pattern3/clip.wav) · 9.59s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A female voice speaks three Chinese sentences, with a brief clicking or croaking sound occurring between the first and second sentences.
- **Why the answer stands** The report describes the first utterance as 'spoken fast' (high), the second as 'spoken slowly' (low), and the third as 'spoken at a medium speed' (medium), which perfectly matches option B.
- **Difficulty** score 0.2518 (auditor answered 5/5 blind, training solver 0.75)

### `prosody-l1-disfluency-type`

- **Question** Which types of disfluencies are present in the audio?
- Filled pauses: e.g., uh, um
- Discourse markers: e.g., well, you know
- Restarts: interrupted or repeated sentence starts
- Explicit editing terms: e.g., I mean
- None: if the speech is fluent.
- **Answer** B. none (fluent speech)
- **Audio** [assets/audio/prosody/prosody-l1-disfluency-type/clip.wav](assets/audio/prosody/prosody-l1-disfluency-type/clip.wav) · 3.08s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man speaks a single sentence about booking a hotel near the airport.
- **Why the answer stands** The report explicitly states that there are no disfluencies present in the speech, which directly supports the claimed answer of 'none (fluent speech)'.
- **Difficulty** score 0.2167 (auditor answered 5/5 blind, training solver 0.75)

### `prosody-l1-speaking-rate`

- **Question** The same person speaks twice. Which utterance is spoken faster?
- **Answer** C. the first one
- **Audio** [assets/audio/prosody/prosody-l1-speaking-rate/clip.wav](assets/audio/prosody/prosody-l1-speaking-rate/clip.wav) · 9.01s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man speaks normally about office coffee, then whispers about a documentary on deep sea creatures.
- **Why the answer stands** The report states that the first segment was spoken at a medium speed while the second segment was spoken slowly, which supports the claim that the first utterance was faster.
- **Difficulty** score 0.1585 (auditor answered 5/5 blind, training solver 0.6666666666666666)

### `prosody-l1-speech-pitch`

- **Question** Which speaker has the higher-pitched voice?
- **Answer** D. the second speaker
- **Audio** [assets/audio/prosody/prosody-l1-speech-pitch/clip.wav](assets/audio/prosody/prosody-l1-speech-pitch/clip.wav) · 5.93s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of two different female voices speaking sentences in Chinese.
- **Why the answer stands** The report explicitly describes the first speaker as having a medium-low pitch and the second speaker as having a high pitch, which supports the claimed answer.
- **Difficulty** score 0.0011 (auditor answered 5/5 blind, training solver 1.0)

### `prosody-l1-compound-speech-reasoning`

- **Question** Which sentence was spoken by the speaker with the highest-pitched voice?
- **Answer** B. We can't afford no nice vittles now when our men are sufferin so.
- **Audio** [assets/audio/prosody/prosody-l1-compound-speech-reasoning/clip.wav](assets/audio/prosody/prosody-l1-compound-speech-reasoning/clip.wav) · 10.76s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features three different speakers—a man, a woman, and a child—each reading a short phrase in succession.
- **Why the answer stands** The report indicates that the third segment, which corresponds to Option B, was spoken by a child's voice with a high pitch, which is the highest pitch among the three speakers.
- **Difficulty** score 0.2363 (auditor answered 5/5 blind, training solver 0.75)

### `prosody-l1-pause-after-word`

- **Question** Where does the speaker stop briefly? Select the word that precedes the pause, or 'No pause'.
- **Answer** C. slept
- **Audio** [assets/audio/prosody/prosody-l1-pause-after-word/clip.wav](assets/audio/prosody/prosody-l1-pause-after-word/clip.wav) · 5.98s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man speaks a sentence with a cough and a filled hesitation in the middle.
- **Why the answer stands** The report explicitly states that there is a pause of about 1.4 seconds after the word 'slept', which directly supports the claimed answer.
- **Difficulty** score 0.2425 (auditor answered 5/5 blind, training solver 0.5)


## Speech Prosody — L2

### `prosody-l2-volume-pattern3`

- **Question** How does the speaker's volume change across the three utterances?
- **Answer** C. low-high-medium
- **Audio** [assets/audio/prosody/prosody-l2-volume-pattern3/clip.wav](assets/audio/prosody/prosody-l2-volume-pattern3/clip.wav) · 13.42s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A speaker delivers three sentences over a continuous background hum, with the first sentence whispered and the subsequent two spoken in a normal voice.
- **Why the answer stands** The report states that Utterance 1 is the quietest (low), Utterance 2 is the loudest (high), and Utterance 3 is middle in loudness (medium), which perfectly matches the claimed answer 'low-high-medium'.
- **Difficulty** score 0.2646 (auditor answered 5/5 blind, training solver 0.5)

### `prosody-l2-disfluency-type`

- **Question** Listen to the speaker. Which disfluency types occur (filled pauses like 'um'; discourse markers like 'well, you know'; restarts; explicit editing terms like 'I mean'), or is the speech fluent?
- **Answer** B. none (fluent speech)
- **Audio** [assets/audio/prosody/prosody-l2-disfluency-type/clip.wav](assets/audio/prosody/prosody-l2-disfluency-type/clip.wav) · 3.08s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A woman speaks the sentence 'She replaced the printer ink cartridge without trouble' against a background of continuous whirring noise.
- **Why the answer stands** The report explicitly states that there are no audible pauses or disfluencies within the speech, which directly supports the claimed answer of 'none (fluent speech)'.
- **Difficulty** score 0.2833 (auditor answered 5/5 blind, training solver 0.75)

### `prosody-l2-speed-pattern3`

- **Question** Which speed pattern best matches the audio?
- **Answer** A. medium-high-low
- **Audio** [assets/audio/prosody/prosody-l2-speed-pattern3/clip.wav](assets/audio/prosody/prosody-l2-speed-pattern3/clip.wav) · 8.64s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of three distinct utterances spoken by female voices with varying loudness, speed, and pitch.
- **Why the answer stands** The report describes the three utterances as being spoken at a medium speed, fast (high), and slowly (low) respectively, which perfectly matches the claimed answer.
- **Difficulty** score 0.2901 (auditor answered 5/5 blind, training solver 0.25)

### `prosody-l2-pause-after-word`

- **Question** Listen for a silent break inside the sentence. Which word comes right before it (or is there no pause)?
- **Answer** C. called
- **Audio** [assets/audio/prosody/prosody-l2-pause-after-word/clip.wav](assets/audio/prosody/prosody-l2-pause-after-word/clip.wav) · 5.65s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man speaks the first phrase of a sentence in a normal voice, pauses, and then whispers the rest of the sentence.
- **Why the answer stands** The report explicitly states that there is a clearly audible silent pause after the word 'called', which directly supports the claimed answer.
- **Difficulty** score 0.2811 (auditor answered 5/5 blind, training solver 0.75)

### `prosody-l2-compound-speech-reasoning`

- **Question** Listen to the three speakers. What does the speaker with the lowest-pitched voice talk about?
- **Answer** A. Till they would finally circle round and round on this morning the buffaloes were very …
- **Audio** [assets/audio/prosody/prosody-l2-compound-speech-reasoning/clip.wav](assets/audio/prosody/prosody-l2-compound-speech-reasoning/clip.wav) · 12.16s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a female voice reading a literary excerpt, followed by a male voice reading a different passage, characterized by clear pauses and a breath intake.
- **Why the answer stands** The report identifies the male voice as having the lowest pitch (low pitch) and transcribes his speech as matching the text in Option A.
- **Difficulty** score 0.2791 (auditor answered 5/5 blind, training solver 0.75)

### `prosody-l2-speaking-rate`

- **Question** How would you describe the speaker's speaking rate?
- **Answer** C. fast
- **Audio** [assets/audio/prosody/prosody-l2-speaking-rate/clip.wav](assets/audio/prosody/prosody-l2-speaking-rate/clip.wav) · 2.36s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man quickly says, 'He filled the bird feeder with sunflower seeds before winter.'
- **Why the answer stands** The report explicitly states that the utterance is spoken at a 'fast speed' and that the man 'quickly says' the sentence, which directly supports option C.
- **Difficulty** score 0.3077 (auditor answered 2/5 blind, training solver 0.8333333333333334)


## Speech Prosody — L3

### `prosody-l3-pitch-pattern3`

- **Question** How does the speaker's voice pitch change across the three parts of the recording?
- **Answer** B. high-low-medium
- **Audio** [assets/audio/prosody/prosody-l3-pitch-pattern3/clip.wav](assets/audio/prosody/prosody-l3-pitch-pattern3/clip.wav) · 11.24s · 10 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features three different voices repeating the phrase 'Plain buns 1729' one after another, with some keyboard typing noise at the start.
- **Why the answer stands** The report explicitly describes the pitch of the three utterances as high, low, and medium, respectively, which perfectly matches option B.
- **Difficulty** score 0.338 (auditor answered 5/5 blind, training solver 0.75)

### `prosody-l3-syllable-count`

- **Question** Count the syllables of the spoken word. Which description is correct?
- **Answer** D. a one-syllable word
- **Audio** [assets/audio/prosody/prosody-l3-syllable-count/clip.wav](assets/audio/prosody/prosody-l3-syllable-count/clip.wav) · 1.38s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A brief crackling hiss is followed by a man saying 'The word is life.'
- **Why the answer stands** The report transcribes the spoken phrase as 'The word is life', which confirms that the target word ('life') is indeed a one-syllable word.
- **Difficulty** score 0.3783 (auditor answered 5/5 blind, training solver 0.5)

### `prosody-l3-speech-pair-compare`

- **Question** Listen to both parts. Which part is spoken faster?
- **Answer** A. the second utterance
- **Audio** [assets/audio/prosody/prosody-l3-speech-pair-compare/clip.wav](assets/audio/prosody/prosody-l3-speech-pair-compare/clip.wav) · 7.8s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A woman reads two statements about a leaking garden hose while water is heard spraying continuously in the background.
- **Why the answer stands** The report states that the first utterance is spoken at a medium speed and the second utterance is spoken at a fast speed, which supports the claimed answer that the second utterance is faster.
- **Difficulty** score 0.3271 (auditor answered 5/5 blind, training solver 0.5)

### `prosody-l3-pause-after-word`

- **Question** Where does the speaker stop briefly? Select the word that precedes the pause, or 'No pause'.
- **Answer** D. steam
- **Audio** [assets/audio/prosody/prosody-l3-pause-after-word/clip.wav](assets/audio/prosody/prosody-l3-pause-after-word/clip.wav) · 4.6s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A female voice speaks the first part of a sentence, followed by a male voice completing it.
- **Why the answer stands** The report divides the transcription into Utterance 1 ending with 'steam' and Utterance 2 starting with 'rose', indicating a boundary/pause after the word 'steam'.
- **Difficulty** score 0.3389 (auditor answered 5/5 blind, training solver 0.0)

### `prosody-l3-volume-pattern3`

- **Question** Which volume pattern best matches the audio?
- **Answer** A. high-low-medium
- **Audio** [assets/audio/prosody/prosody-l3-volume-pattern3/clip.wav](assets/audio/prosody/prosody-l3-volume-pattern3/clip.wav) · 12.04s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A male speaker delivers two distinct spoken passages separated by a brief pause.
- **Why the answer stands** The report describes Utterance 1 as the loudest (high), followed by a silence (low), and Utterance 2 as having middle loudness (medium), which perfectly matches the pattern 'high-low-medium'.
- **Difficulty** score 0.3346 (auditor answered 5/5 blind, training solver 0.25)

### `prosody-l3-speaking-rate`

- **Question** How would you describe the speaker's speaking rate?
- **Answer** A. fast
- **Audio** [assets/audio/prosody/prosody-l3-speaking-rate/clip.wav](assets/audio/prosody/prosody-l3-speaking-rate/clip.wav) · 2.02s · 5 tools
- **Quality** pass A 4/5 (acceptable), pass B 5/5 (showcase)
- **Heard, blind** A man quickly says 'less than half of three eggs and a cup of flour'.
- **Why the answer stands** The listener's report explicitly states that the utterance is spoken at a 'fast pace' and that the man 'quickly says' the phrase, which directly supports the claimed answer 'A. fast'.
- **Difficulty** score 0.3846 (auditor answered 2/5 blind, training solver 0.6666666666666666)


## Speech Prosody — L4

### `prosody-l4-pitch-pattern3`

- **Question** Listen to the three segments. What is the pitch pattern from the first to the third?
- **Answer** D. high-low-medium
- **Audio** [assets/audio/prosody/prosody-l4-pitch-pattern3/clip.wav](assets/audio/prosody/prosody-l4-pitch-pattern3/clip.wav) · 15.7s · 10 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains three successive readings of the sentence 'Old dances are simplified of their yearning, bleached by time' by a high-pitched female voice, a low-pitched male voice, and a medium-pitched female voice, respectively.
- **Why the answer stands** The report explicitly describes the pitch of the three utterances as high, low, and medium, respectively, which perfectly matches option D.
- **Difficulty** score 0.4164 (auditor answered 5/5 blind, training solver 0.5)

### `prosody-l4-syllable-count`

- **Question** The speaker says a single word. How many syllables does it have?
- **Answer** D. a two-syllable word
- **Audio** [assets/audio/prosody/prosody-l4-syllable-count/clip.wav](assets/audio/prosody/prosody-l4-syllable-count/clip.wav) · 1.86s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The recording contains a sharp intake of breath followed by a woman saying 'The word is little'.
- **Why the answer stands** The report transcribes the utterance as 'The word is little', and the target word 'little' has two syllables, which supports the claimed answer.
- **Difficulty** score 0.4017 (auditor answered 5/5 blind, training solver 0.5)

### `prosody-l4-speech-pair-compare`

- **Question** Listen to both parts. Which part is louder?
- **Answer** A. both are about the same
- **Audio** [assets/audio/prosody/prosody-l4-speech-pair-compare/clip.wav](assets/audio/prosody/prosody-l4-speech-pair-compare/clip.wav) · 8.3s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A female voice speaks two sentences over a light acoustic background music track.
- **Why the answer stands** The report describes both the first and second utterances as having 'middle loudness', which supports the claim that both are about the same.
- **Difficulty** score 0.4525 (auditor answered 4/5 blind, training solver 0.0)

### `prosody-l4-pause-after-word`

- **Question** Listen for a silent break inside the sentence. Which word comes right before it (or is there no pause)?
- **Answer** A. organizing
- **Audio** [assets/audio/prosody/prosody-l4-pause-after-word/clip.wav](assets/audio/prosody/prosody-l4-pause-after-word/clip.wav) · 4.88s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A single speaker reads a sentence about organizing a garage, with a brief pause in the middle.
- **Why the answer stands** The report explicitly states that a silent pause occurs after the word 'organizing', which directly supports the claimed answer.
- **Difficulty** score 0.3917 (auditor answered 5/5 blind, training solver 0.25)

### `prosody-l4-speaking-rate`

- **Question** The same person speaks twice. Which utterance is spoken faster?
- **Answer** C. the first one
- **Audio** [assets/audio/prosody/prosody-l4-speaking-rate/clip.wav](assets/audio/prosody/prosody-l4-speaking-rate/clip.wav) · 9.21s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A male voice speaks one sentence at a normal volume and then whispers a second sentence.
- **Why the answer stands** The report states that the first segment is spoken at a 'medium speed' and the second at a 'medium-to-slow speed', which supports the claim that the first utterance is faster.
- **Difficulty** score 0.3895 (auditor answered 5/5 blind, training solver 0.16666666666666666)

### `prosody-l4-volume-pattern3`

- **Question** Which volume pattern best matches the audio?
- **Answer** A. medium-high-low
- **Audio** [assets/audio/prosody/prosody-l4-volume-pattern3/clip.wav](assets/audio/prosody/prosody-l4-volume-pattern3/clip.wav) · 12.94s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of three separate sentences spoken by a male voice with short pauses in between.
- **Why the answer stands** The report describes Utterance 1 as having 'middle loudness', Utterance 2 as 'the loudest', and Utterance 3 as 'the quietest', which perfectly matches the 'medium-high-low' volume pattern of Option A.
- **Difficulty** score 0.4048 (auditor answered 3/5 blind, training solver 0.25)


## Speech Prosody — L5

### `prosody-l5-speech-pair-compare`

- **Question** Two sentences are spoken by one speaker. Which one is louder?
- **Answer** D. both are about the same
- **Audio** [assets/audio/prosody/prosody-l5-speech-pair-compare/clip.wav](assets/audio/prosody/prosody-l5-speech-pair-compare/clip.wav) · 7.9s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man reads two sentences with the sound of a drawer closing occurring in the brief pause between them.
- **Why the answer stands** The report states that both utterances are spoken with 'middle loudness', which supports the claim that they are about the same loudness.
- **Difficulty** score 0.6105 (auditor answered 4/5 blind, training solver 0.0)

### `prosody-l5-syllable-count`

- **Question** How many syllables are in the word you heard?
- **Answer** A. a five-syllable word
- **Audio** [assets/audio/prosody/prosody-l5-syllable-count/clip.wav](assets/audio/prosody/prosody-l5-syllable-count/clip.wav) · 2.03s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man says 'The word is bilateralism' surrounded by applause.
- **Why the answer stands** The report states the 8-syllable phrase is 'The word is bilateralism', which leaves exactly 5 syllables for the word 'bilateralism' after subtracting the 3 syllables of 'The word is'.
- **Difficulty** score 0.4767 (auditor answered 0/5 blind, training solver 0.75)

### `prosody-l5-volume-pattern3`

- **Question** Listen to the three parts. What is the loudness pattern from the first to the third?
- **Answer** A. medium-low-high
- **Audio** [assets/audio/prosody/prosody-l5-volume-pattern3/clip.wav](assets/audio/prosody/prosody-l5-volume-pattern3/clip.wav) · 9.5s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A male voice reads three literary sentences with varying pitch, speed, and loudness.
- **Why the answer stands** The report describes the first utterance as having 'middle loudness', the second as 'the quietest' (low), and the third as 'the loudest' (high), which perfectly matches the pattern 'medium-low-high' in option A.
- **Difficulty** score 0.4991 (auditor answered 2/5 blind, training solver 0.25)

### `prosody-l5-pause-after-word`

- **Question** Where does the speaker stop briefly? Select the word that precedes the pause, or 'No pause'.
- **Answer** D. stove
- **Audio** [assets/audio/prosody/prosody-l5-pause-after-word/clip.wav](assets/audio/prosody/prosody-l5-pause-after-word/clip.wav) · 4.33s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man speaks a sentence with a pause in the middle.
- **Why the answer stands** The report explicitly states that there is a clearly audible silent pause after the word 'stove', which directly supports the claimed answer.
- **Difficulty** score 0.5 (auditor answered 5/5 blind, training solver 0.0)

### `prosody-l5-disfluency`

- **Question** Which speaker hesitates with fillers like 'um' or 'uh'?
- **Answer** B. the man
- **Audio** [assets/audio/prosody/prosody-l5-disfluency/clip.wav](assets/audio/prosody/prosody-l5-disfluency/clip.wav) · 16.51s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of four spoken sentences alternating between male and female voices.
- **Why the answer stands** The report notes that the male speaker used the disfluency 'you know' (a filler like 'um' or 'uh') in both of his utterances, while the female speaker did not.
- **Difficulty** score 0.5517 (auditor answered 0/5 blind, training solver 0.6666666666666666)

### `prosody-l5-speaking-rate`

- **Question** What is the pace of the speech?
- **Answer** A. fast
- **Audio** [assets/audio/prosody/prosody-l5-speaking-rate/clip.wav](assets/audio/prosody/prosody-l5-speaking-rate/clip.wav) · 2.07s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man quickly says, 'A layer of frost covered the car windshield.'
- **Why the answer stands** The report explicitly states that the utterance is spoken 'quickly', which directly supports the claimed answer 'fast'.
- **Difficulty** score 0.6923 (auditor answered 1/5 blind, training solver 0.16666666666666666)


## Sound Events — L1

### `sound-l1-sound-reasoning-real`

- **Question** What most likely happened right after the alarm clock rang?
- **Answer** B. The person used the bathroom and then groomed.
- **Audio** [assets/audio/sound/sound-l1-sound-reasoning-real/clip.wav](assets/audio/sound/sound-l1-sound-reasoning-real/clip.wav) · 18.96s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a sequence of household sounds including a digital alarm, splashing water, a loud buzzer, and crinkling plastic, all over a continuous low background hum.
- **Why the answer stands** The report describes a digital alarm at 0.0s followed immediately by water splashing and sloshing at 2.0s and an electric buzzer (likely a shaver or toothbrush) at 4.0s, which directly supports the sequence of waking up, using the bathroom, and grooming.
- **Difficulty** score 0.0774 (auditor answered 5/5 blind, training solver 1.0)

### `sound-l1-sound-order-real`

- **Question** Which sound is heard last?
- **Answer** C. burp
- **Audio** [assets/audio/sound/sound-l1-sound-order-real/clip.wav](assets/audio/sound/sound-l1-sound-order-real/clip.wav) · 7.23s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a short toy accordion melody, a single bell ding, and a loud human belch.
- **Why the answer stands** The report states that the last sound heard is a loud human belch at 5.0s, which is a synonym for burp.
- **Difficulty** score 0.0945 (auditor answered 5/5 blind, training solver 1.0)

### `sound-l1-sound-loudness`

- **Question** Which sound is louder?
- **Answer** C. Run
- **Audio** [assets/audio/sound/sound-l1-sound-loudness/clip.wav](assets/audio/sound/sound-l1-sound-loudness/clip.wav) · 4.66s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains the sound of rapid footsteps on gravel followed by a single metallic clink.
- **Why the answer stands** The report explicitly states that the footsteps (which correspond to 'Run') are the loudest sound event, while the metallic clink is quieter.
- **Difficulty** score 0.0769 (auditor answered 4/5 blind, training solver 1.0)

### `sound-l1-audioset-sound-id`

- **Question** Identify the sound heard in this recording.
- **Answer** B. siren
- **Audio** [assets/audio/sound/sound-l1-audioset-sound-id/clip.wav](assets/audio/sound/sound-l1-audioset-sound-id/clip.wav) · 10.4s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A mechanical air-raid siren wails continuously, rising and falling in pitch and volume over ten seconds.
- **Why the answer stands** The listener's report explicitly and repeatedly identifies the sound as a mechanical air-raid siren, which directly supports the claimed answer.
- **Difficulty** score 0.1099 (auditor answered 5/5 blind, training solver 1.0)

### `sound-l1-sound-id-real`

- **Question** Identify the sound heard in this recording.
- **Answer** A. gong
- **Audio** [assets/audio/sound/sound-l1-sound-id-real/clip.wav](assets/audio/sound/sound-l1-sound-id-real/clip.wav) · 1.72s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A single high-pitched metallic chime, like a triangle or service bell, strikes once and decays.
- **Why the answer stands** The report describes a single metallic strike with a long decay, which supports the 'gong' option as it is the only metallic percussion instrument among the choices.
- **Difficulty** score 0.1554 (auditor answered 5/5 blind, training solver 0.75)

### `sound-l1-sound-change-real`

- **Question** What happens halfway through the clip?
- **Answer** D. the pen writing stops and the airplane starts
- **Audio** [assets/audio/sound/sound-l1-sound-change-real/clip.wav](assets/audio/sound/sound-l1-sound-change-real/clip.wav) · 12.06s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features the sound of a marker writing on a whiteboard, followed by a low background rumble, a resonant metallic chime, and a digital two-tone notification chime.
- **Why the answer stands** The report states that the marker writing lasts about 4 seconds (stopping at 4.0s) and a low background rumble (representing the airplane) starts at 4.0s, which perfectly matches the transition described in the correct option.
- **Difficulty** score 0.1061 (auditor answered 5/5 blind, training solver 1.0)


## Sound Events — L2

### `sound-l2-sound-reasoning-real`

- **Question** Where does this scene most likely take place?
- **Answer** A. Bedroom and bathroom
- **Audio** [assets/audio/sound/sound-l2-sound-reasoning-real/clip.wav](assets/audio/sound/sound-l2-sound-reasoning-real/clip.wav) · 21.95s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio captures a morning wake-up routine, featuring an alarm clock, a yawn, drinking, and splashing water.
- **Why the answer stands** The report describes waking up to an alarm clock and yawning (associated with a bedroom) followed by gurgling and splashing water (associated with a bathroom), which directly supports the 'Bedroom and bathroom' option.
- **Difficulty** score 0.1715 (auditor answered 5/5 blind, training solver 0.75)

### `sound-l2-scene-inference`

- **Question** Which location best matches the sounds you hear?
- **Answer** C. a farmyard
- **Audio** [assets/audio/sound/sound-l2-scene-inference/clip.wav](assets/audio/sound/sound-l2-scene-inference/clip.wav) · 4.86s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a sharp metallic clink, followed by birds chirping and a dog howling in the distance.
- **Why the answer stands** The report describes birds chirping and a dog howling in a quiet rural or suburban environment, which strongly supports a farmyard over the other options.
- **Difficulty** score 0.2308 (auditor answered 5/5 blind, training solver 0.5)

### `sound-l2-sound-order-real`

- **Question** What is the final sound in the clip?
- **Answer** B. thunder
- **Audio** [assets/audio/sound/sound-l2-sound-order-real/clip.wav](assets/audio/sound/sound-l2-sound-order-real/clip.wav) · 7.8s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of three consecutive sound effects: a child laughing, a toilet flushing, and a low rumble of thunder.
- **Why the answer stands** The report lists the events in chronological order, with the final sound starting at 5.0s described as a low rumble of thunder, which directly supports the claimed answer.
- **Difficulty** score 0.1783 (auditor answered 5/5 blind, training solver 0.75)

### `sound-l2-sound-id-real`

- **Question** Which of the following best describes the sound in the clip?
- **Answer** B. screech
- **Audio** [assets/audio/sound/sound-l2-sound-id-real/clip.wav](assets/audio/sound/sound-l2-sound-id-real/clip.wav) · 3.78s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a single, continuous high-pitched squeaking or friction sound lasting just over one second.
- **Why the answer stands** The report describes a high-pitched squeaking or rubber friction sound, which is well-characterized by the term 'screech' and does not match any of the other options.
- **Difficulty** score 0.2188 (auditor answered 5/5 blind, training solver 0.75)

### `sound-l2-sound-louder-real`

- **Question** Of the two sounds in the clip, which one is louder?
- **Answer** B. crushing
- **Audio** [assets/audio/sound/sound-l2-sound-louder-real/clip.wav](assets/audio/sound/sound-l2-sound-louder-real/clip.wav) · 4.2s · 4 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains the sound of plastic crinkling followed by a short sequence of footsteps on a wooden floor.
- **Why the answer stands** The report explicitly states that the loudest sound is the plastic crinkling at the beginning, which corresponds to the 'crushing' option.
- **Difficulty** score 0.1667 (auditor answered 5/5 blind, training solver 0.75)

### `sound-l2-sound-count`

- **Question** Count the occurrences of the harmonica sound.
- **Answer** A. 6
- **Audio** [assets/audio/sound/sound-l2-sound-count/clip.wav](assets/audio/sound/sound-l2-sound-count/clip.wav) · 13.7s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a solo harmonica playing a series of sustained notes and pitch bends.
- **Why the answer stands** The report explicitly states that the harmonica plays 6 distinct notes or phrases and lists 6 separate events.
- **Difficulty** score 0.1639 (auditor answered 4/5 blind, training solver 0.8333333333333334)


## Sound Events — L3

### `sound-l3-audioset-sound-id`

- **Question** What is the source of the sound in this audio?
- **Answer** C. car horn
- **Audio** [assets/audio/sound/sound-l3-audioset-sound-id/clip.wav](assets/audio/sound/sound-l3-audioset-sound-id/clip.wav) · 10.4s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features the sounds of traffic on a street, including a car driving past and a car horn honking twice at the beginning and near the end.
- **Why the answer stands** The report explicitly and repeatedly mentions a car horn honking, which directly supports option C.
- **Difficulty** score 0.2491 (auditor answered 5/5 blind, training solver 1.0)

### `sound-l3-sound-louder-real`

- **Question** Which sound is played at the higher volume?
- **Answer** D. finger snap
- **Audio** [assets/audio/sound/sound-l3-sound-louder-real/clip.wav](assets/audio/sound/sound-l3-sound-louder-real/clip.wav) · 3.47s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a sudden gasp of breath followed by a sharp finger snap.
- **Why the answer stands** The report explicitly states that the finger snap is the loudest sound, which directly supports the claimed answer.
- **Difficulty** score 0.3171 (auditor answered 3/5 blind, training solver 0.75)

### `sound-l3-sound-reasoning-real`

- **Question** Where does this scene most likely take place?
- **Answer** D. In a bathroom
- **Audio** [assets/audio/sound/sound-l3-sound-reasoning-real/clip.wav](assets/audio/sound/sound-l3-sound-reasoning-real/clip.wav) · 14.22s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features a sequence of domestic sounds including a baby crying, an engine idling, a hair dryer blowing, a door slamming, and rapid thumping.
- **Why the answer stands** The report mentions a hair dryer blowing in an indoor domestic setting, which strongly points to a bathroom as the most likely location among the choices.
- **Difficulty** score 0.3179 (auditor answered 3/5 blind, training solver 1.0)

### `sound-l3-sound-id-real`

- **Question** Identify the sound heard in this recording.
- **Answer** A. crash cymbal
- **Audio** [assets/audio/sound/sound-l3-sound-id-real/clip.wav](assets/audio/sound/sound-l3-sound-id-real/clip.wav) · 5.61s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a single cymbal crash accompanied by a low-frequency wind whoosh, both fading out over five seconds.
- **Why the answer stands** The listener's report explicitly identifies a 'cymbal crash' as the primary sound in the recording, which directly supports the claimed answer of 'crash cymbal'.
- **Difficulty** score 0.2571 (auditor answered 5/5 blind, training solver 0.75)

### `sound-l3-sound-duration`

- **Question** Which sound lasts longer?
- **Answer** A. Burping, eructation
- **Audio** [assets/audio/sound/sound-l3-sound-duration/clip.wav](assets/audio/sound/sound-l3-sound-duration/clip.wav) · 6.91s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains two quick scraping sounds followed by a loud, deep burp.
- **Why the answer stands** The report explicitly states that the scraping sounds last under a second each, whereas the burp is noticeably longer, lasting nearly two seconds, which directly supports option A.
- **Difficulty** score 0.233 (auditor answered 3/5 blind, training solver 0.8333333333333334)

### `sound-l3-sound-category`

- **Question** Which category best describes the sound source?
- **Answer** C. an animal
- **Audio** [assets/audio/sound/sound-l3-sound-category/clip.wav](assets/audio/sound/sound-l3-sound-category/clip.wav) · 2.0s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features the continuous, lively chirping of birds in an outdoor setting.
- **Why the answer stands** The report explicitly identifies the sound source as birds chirping, which directly supports the category of 'an animal'.
- **Difficulty** score 0.3077 (auditor answered 5/5 blind, training solver 0.3333333333333333)


## Sound Events — L4

### `sound-l4-sound-louder-real`

- **Question** Which of the two sounds is louder?
- **Answer** D. jingle bell
- **Audio** [assets/audio/sound/sound-l4-sound-louder-real/clip.wav](assets/audio/sound/sound-l4-sound-louder-real/clip.wav) · 6.5s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features continuous background crickets, accompanied by a brief metallic clinking sound and a single dull thud.
- **Why the answer stands** The report states that the loudest sound is the metallic clinking (corresponding to the jingle bell), followed by the dull thud (corresponding to the bass drum), which supports the claimed answer.
- **Difficulty** score 0.3761 (auditor answered 4/5 blind, training solver 0.25)

### `sound-l4-sound-category`

- **Question** What kind of source most likely produced the main sound?
- **Answer** A. a household object or appliance
- **Audio** [assets/audio/sound/sound-l4-sound-category/clip.wav](assets/audio/sound/sound-l4-sound-category/clip.wav) · 2.02s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists entirely of a single, short sound of adhesive packing tape being pulled from a roll.
- **Why the answer stands** The report identifies the sound as adhesive packing tape being pulled off a roll, which is a common household object.
- **Difficulty** score 0.3846 (auditor answered 5/5 blind, training solver 0.16666666666666666)

### `sound-l4-audioset-sound-id`

- **Question** Which of the following best describes the sound in the clip?
- **Answer** D. drill
- **Audio** [assets/audio/sound/sound-l4-audioset-sound-id/clip.wav](assets/audio/sound/sound-l4-audioset-sound-id/clip.wav) · 10.4s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A man explains how to change a power tool bit over background music, preceded by the sound of the tool running.
- **Why the answer stands** The report describes a power tool whirring, changing a 'bit' and a 'spade', and switching to 'chisel only', which strongly supports the option 'drill'.
- **Difficulty** score 0.4265 (auditor answered 5/5 blind, training solver 0.25)

### `sound-l4-sound-timing`

- **Question** Roughly how much time passes between the cellphone buzz sound and the crushing sound?
- **Answer** D. about 1 second
- **Audio** [assets/audio/sound/sound-l4-sound-timing/clip.wav](assets/audio/sound/sound-l4-sound-timing/clip.wav) · 4.14s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains a brief phone vibration followed by the sound of plastic packaging rustling.
- **Why the answer stands** The report states that the phone vibrates at 0.0s and the plastic packaging rustles at 1.0s, which directly supports the claimed answer of about 1 second.
- **Difficulty** score 0.3846 (auditor answered 2/5 blind, training solver 0.6666666666666666)

### `sound-l4-sound-count`

- **Question** How many times do you hear the glockenspiel sound?
- **Answer** B. 6
- **Audio** [assets/audio/sound/sound-l4-sound-count/clip.wav](assets/audio/sound/sound-l4-sound-count/clip.wav) · 12.76s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of a descending sequence of paired synthesizer bell chimes followed by a rapid, ascending harp-like glissando.
- **Why the answer stands** The report describes three pairs of synthesizer bell chimes, making a total of six bell chime sounds, which corresponds to the six glockenspiel sounds in the claimed answer.
- **Difficulty** score 0.3936 (auditor answered 4/5 blind, training solver 0.3333333333333333)

### `sound-l4-sound-change-real`

- **Question** How does the audio change in the middle of the recording?
- **Answer** D. the pen writing stops and the clapping starts
- **Audio** [assets/audio/sound/sound-l4-sound-change-real/clip.wav](assets/audio/sound/sound-l4-sound-change-real/clip.wav) · 11.94s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains a sequence of a scratching sound, a loud clap, and water splashing.
- **Why the answer stands** The report describes a scratching sound (pen writing) that lasts for 4.5 seconds and is immediately followed by a sharp clap at 4.5 seconds, which directly supports option D.
- **Difficulty** score 0.3906 (auditor answered 5/5 blind, training solver 0.0)


## Sound Events — L5

### `sound-l5-audioset-sound-id`

- **Question** What is the source of the sound in this audio?
- **Answer** C. goose
- **Audio** [assets/audio/sound/sound-l5-audioset-sound-id/clip.wav](assets/audio/sound/sound-l5-audioset-sound-id/clip.wav) · 10.4s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A person walks on gravel outdoors while brief clapping, a short spoken phrase, and distant geese honking are heard.
- **Why the answer stands** The report explicitly mentions 'geese honking' as one of the sounds heard in the audio, which directly supports the claimed answer of 'goose'.
- **Difficulty** score 0.5649 (auditor answered 5/5 blind, training solver 0.0)

### `sound-l5-sound-duration`

- **Question** Which sound lasts longer?
- **Answer** C. Baby laughter
- **Audio** [assets/audio/sound/sound-l5-sound-duration/clip.wav](assets/audio/sound/sound-l5-sound-duration/clip.wav) · 4.7s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains a baby laughing followed by a low-pitched vibration sound.
- **Why the answer stands** The report explicitly states that the baby's laughter lasts about 2 seconds, which is longer than the vibration sound's duration of 1.5 seconds.
- **Difficulty** score 0.5385 (auditor answered 4/5 blind, training solver 0.0)

### `sound-l5-sound-count-real`

- **Question** In this recording, how many car passing by events occur?
- **Answer** B. 5
- **Audio** [assets/audio/sound/sound-l5-sound-count-real/clip.wav](assets/audio/sound/sound-l5-sound-count-real/clip.wav) · 30.13s · 6 tools
- **Quality** pass A 4/5 (acceptable), pass B 5/5 (showcase)
- **Heard, blind** The audio captures the steady sound of rain or water spraying with intermittent sounds of vehicles driving past on a wet road.
- **Why the answer stands** The report explicitly lists five vehicle passing events and states there are 'five distinct vehicle pass sounds', which directly supports option B.
- **Difficulty** score 0.5288 (auditor answered 5/5 blind, training solver 0.0)

### `sound-l5-sound-order-real`

- **Question** Which sound is heard second?
- **Answer** D. bass guitar
- **Audio** [assets/audio/sound/sound-l5-sound-order-real/clip.wav](assets/audio/sound/sound-l5-sound-order-real/clip.wav) · 10.47s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of three distinct sounds in sequence: a metallic clicking, a short bass guitar riff, and a single chime strike.
- **Why the answer stands** The report explicitly states that the second sound in the sequence is a bass guitar riff starting at 2.0 seconds.
- **Difficulty** score 0.6388 (auditor answered 0/5 blind, training solver 0.0)

### `sound-l5-sound-count`

- **Question** Count the occurrences of the chirp sound.
- **Answer** D. 4
- **Audio** [assets/audio/sound/sound-l5-sound-count/clip.wav](assets/audio/sound/sound-l5-sound-count/clip.wav) · 3.97s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A bird sings with four distinct series of high-pitched chirps in a quiet outdoor setting.
- **Why the answer stands** The report explicitly states there are four distinct chirping phrases and lists four timestamps for the chirping sound, which directly supports the claimed answer of 4.
- **Difficulty** score 0.5385 (auditor answered 0/5 blind, training solver 0.6666666666666666)

### `sound-l5-sound-id-real`

- **Question** What sound is this?
- **Answer** C. shuffling cards
- **Audio** [assets/audio/sound/sound-l5-sound-id-real/clip.wav](assets/audio/sound/sound-l5-sound-id-real/clip.wav) · 4.65s · 5 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A deck of playing cards is shuffled using a riffle and cascade technique.
- **Why the answer stands** The listener's report explicitly describes the sound of a deck of playing cards being shuffled, which directly supports the claimed answer.
- **Difficulty** score 0.4846 (auditor answered 3/5 blind, training solver 0.25)


## Speakers & Dialogue — L1

### `speakers-l1-dialogue-turns`

- **Question** How many times does someone take the floor in this dialogue? Count each uninterrupted stretch by one speaker as one turn.
- **Answer** B. 2
- **Audio** [assets/audio/speakers/speakers-l1-dialogue-turns/clip.wav](assets/audio/speakers/speakers-l1-dialogue-turns/clip.wav) · 10.25s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** Two different women take turns reading literary descriptions in English.
- **Why the answer stands** The report states there are two distinct speakers with one transition at 5.0 seconds and neither voice recurring, which confirms that there are exactly two turns.
- **Difficulty** score 0.1173 (auditor answered 5/5 blind, training solver 1.0)

### `speakers-l1-speaker-count`

- **Question** Count the number of different voices.
- **Answer** A. 1
- **Audio** [assets/audio/speakers/speakers-l1-speaker-count/clip.wav](assets/audio/speakers/speakers-l1-speaker-count/clip.wav) · 4.4s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult man reads a sentence about Sister Helen making a wax figure.
- **Why the answer stands** The report explicitly states that there is only one distinct speaker and no other voices are present, which directly supports the claimed answer of 1.
- **Difficulty** score 0.0778 (auditor answered 5/5 blind, training solver 1.0)

### `speakers-l1-turn-order`

- **Question** How many speaking turns are there in total?
- **Answer** A. 5
- **Audio** [assets/audio/speakers/speakers-l1-turn-order/clip.wav](assets/audio/speakers/speakers-l1-turn-order/clip.wav) · 24.69s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A conversation in Mandarin Chinese between three people discussing a dentist appointment and plans to eat hotpot afterwards.
- **Why the answer stands** The report explicitly states that there are 5 turns in total, which directly supports option A.
- **Difficulty** score 0.0996 (auditor answered 5/5 blind, training solver 0.8333333333333334)

### `speakers-l1-dialogue-turns-real`

- **Question** In this real conversation, how many speaking turns occur in total?
- **Answer** C. 4
- **Audio** [assets/audio/speakers/speakers-l1-dialogue-turns-real/clip.wav](assets/audio/speakers/speakers-l1-dialogue-turns-real/clip.wav) · 11.16s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** Three different speakers repeat two sentences about dogs and kids by the door.
- **Why the answer stands** The report lists four distinct speech events with timestamps and transcriptions, which supports the claimed answer of 4 speaking turns.
- **Difficulty** score 0.1487 (auditor answered 5/5 blind, training solver 0.75)

### `speakers-l1-speaker-gender`

- **Question** How many female voices take part in this conversation?
- **Answer** A. 2
- **Audio** [assets/audio/speakers/speakers-l1-speaker-gender/clip.wav](assets/audio/speakers/speakers-l1-speaker-gender/clip.wav) · 26.19s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of four different speakers taking turns reading unrelated English sentences.
- **Why the answer stands** The report explicitly states that there are four distinct speakers, including two adult women (Speaker 1 and Speaker 4).
- **Difficulty** score 0.1783 (auditor answered 5/5 blind, training solver 0.6666666666666666)

### `speakers-l1-real-speaker-count`

- **Question** How many of the speakers are women?
- **Answer** C. 0
- **Audio** [assets/audio/speakers/speakers-l1-real-speaker-count/clip.wav](assets/audio/speakers/speakers-l1-real-speaker-count/clip.wav) · 8.53s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains two different men speaking in English, one with a British accent and the other with an American accent.
- **Why the answer stands** The report explicitly states that both speakers in the recording are adult men, which supports the claimed answer of 0 women speakers.
- **Difficulty** score 0.0041 (auditor answered 5/5 blind, training solver 1.0)


## Speakers & Dialogue — L2

### `speakers-l2-dialogue-turns`

- **Question** Count the speaker turns in this conversation (a turn ends whenever a different speaker starts talking). How many are there?
- **Answer** B. 4
- **Audio** [assets/audio/speakers/speakers-l2-dialogue-turns/clip.wav](assets/audio/speakers/speakers-l2-dialogue-turns/clip.wav) · 22.52s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult man and an adult woman take turns reading various sentences in English over a continuous background sound of rhythmic marching footsteps.
- **Why the answer stands** The report states that the speaker changes 3 times (Man to Woman, Woman to Man, and Man to Woman), which corresponds to exactly 4 speaker turns.
- **Difficulty** score 0.2394 (auditor answered 5/5 blind, training solver 0.75)

### `speakers-l2-language-id`

- **Question** Which language is spoken in the recording?
- **Answer** C. Japanese
- **Audio** [assets/audio/speakers/speakers-l2-language-id/clip.wav](assets/audio/speakers/speakers-l2-language-id/clip.wav) · 3.23s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult woman speaks a single sentence in Japanese with the sound of rain falling in the background.
- **Why the answer stands** The listener's report explicitly states multiple times that the speaker is speaking in Japanese, which directly supports the claimed answer.
- **Difficulty** score 0.2483 (auditor answered 5/5 blind, training solver 1.0)

### `speakers-l2-speaker-count`

- **Question** How many different speakers can be heard?
- **Answer** A. 4
- **Audio** [assets/audio/speakers/speakers-l2-speaker-count/clip.wav](assets/audio/speakers/speakers-l2-speaker-count/clip.wav) · 14.95s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio is a compilation of four different English-speaking voices reading short sentences.
- **Why the answer stands** The report explicitly states that there are four distinct speakers in the recording.
- **Difficulty** score 0.2629 (auditor answered 4/5 blind, training solver 0.75)

### `speakers-l2-dialogue-turns-real`

- **Question** Count the speaker turns in the dialogue (a turn ends whenever a different speaker starts talking). How many are there?
- **Answer** A. 2
- **Audio** [assets/audio/speakers/speakers-l2-dialogue-turns-real/clip.wav](assets/audio/speakers/speakers-l2-dialogue-turns-real/clip.wav) · 4.71s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains two adult men speaking in English, one after the other, about kids talking by the door and a car breaking down.
- **Why the answer stands** The report states there are two distinct speakers speaking one after the other, which corresponds to 2 speaker turns.
- **Difficulty** score 0.2528 (auditor answered 5/5 blind, training solver 0.75)

### `speakers-l2-turn-order`

- **Question** Count how many times a different person takes over speaking.
- **Answer** A. 5
- **Audio** [assets/audio/speakers/speakers-l2-turn-order/clip.wav](assets/audio/speakers/speakers-l2-turn-order/clip.wav) · 24.43s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult woman and an adult man have a conversation about a surprise birthday visit.
- **Why the answer stands** The report explicitly states that there are 5 speaker changes, which directly supports the claimed answer of 5.
- **Difficulty** score 0.2532 (auditor answered 5/5 blind, training solver 0.5)

### `speakers-l2-speaker-gender`

- **Question** How many female voices take part in this conversation?
- **Answer** A. 2
- **Audio** [assets/audio/speakers/speakers-l2-speaker-gender/clip.wav](assets/audio/speakers/speakers-l2-speaker-gender/clip.wav) · 16.17s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** Two adult women take turns reading four short, unrelated sentences in English.
- **Why the answer stands** The report explicitly states that there are two distinct speakers in the recording, both sounding like adult women, which directly supports the claimed answer of 2.
- **Difficulty** score 0.2437 (auditor answered 5/5 blind, training solver 0.5)


## Speakers & Dialogue — L3

### `speakers-l3-language-id`

- **Question** In which language is this sentence spoken?
- **Answer** B. Japanese
- **Audio** [assets/audio/speakers/speakers-l3-language-id/clip.wav](assets/audio/speakers/speakers-l3-language-id/clip.wav) · 4.84s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult woman sighs and pants, then speaks a single sentence in Japanese.
- **Why the answer stands** The listener's report explicitly states that the speaker speaks in Japanese, which directly supports the claimed answer.
- **Difficulty** score 0.3233 (auditor answered 5/5 blind, training solver 0.75)

### `speakers-l3-dialogue-turns`

- **Question** In this exchange, how many speaking turns occur in total?
- **Answer** B. 4
- **Audio** [assets/audio/speakers/speakers-l3-dialogue-turns/clip.wav](assets/audio/speakers/speakers-l3-dialogue-turns/clip.wav) · 20.32s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult male and an adult female take turns reading sentences in English over a continuous background sound of rhythmic mechanical sliding.
- **Why the answer stands** The report explicitly states that there are 4 conversational turns, which directly supports the claimed answer of 4.
- **Difficulty** score 0.2748 (auditor answered 5/5 blind, training solver 0.75)

### `speakers-l3-speaker-count`

- **Question** How many distinct people speak in this recording?
- **Answer** D. 1
- **Audio** [assets/audio/speakers/speakers-l3-speaker-count/clip.wav](assets/audio/speakers/speakers-l3-speaker-count/clip.wav) · 4.5s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult man speaks a short sentence in English with no other sounds.
- **Why the answer stands** The report explicitly states that there is only one speaker, which directly supports the claimed answer of 1.
- **Difficulty** score 0.3389 (auditor answered 5/5 blind, training solver 0.25)

### `speakers-l3-dialogue-turns-real`

- **Question** In this real conversation, how many speaking turns occur in total?
- **Answer** B. 2
- **Audio** [assets/audio/speakers/speakers-l3-dialogue-turns-real/clip.wav](assets/audio/speakers/speakers-l3-dialogue-turns-real/clip.wav) · 6.52s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult man says 'Dogs are sitting by the door' in a crying voice, and another adult man responds calmly with 'No, I know. But still,' followed by a sigh.
- **Why the answer stands** The report explicitly states that there are 'two conversational turns total', which directly supports the claimed answer of 2 (Option B).
- **Difficulty** score 0.3596 (auditor answered 5/5 blind, training solver 0.5)

### `speakers-l3-turn-order`

- **Question** Count how many times a different person takes over speaking.
- **Answer** C. 3
- **Audio** [assets/audio/speakers/speakers-l3-turn-order/clip.wav](assets/audio/speakers/speakers-l3-turn-order/clip.wav) · 34.22s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** Two adult women are having a conversation in Mandarin Chinese about planning a dinner at a newly opened Italian restaurant.
- **Why the answer stands** The report explicitly states that there are 3 speaker changes, which directly supports the claimed answer of 3.
- **Difficulty** score 0.3414 (auditor answered 5/5 blind, training solver 0.3333333333333333)

### `speakers-l3-real-speaker-count`

- **Question** How many different speakers can be heard in this recording?
- **Answer** A. 3
- **Audio** [assets/audio/speakers/speakers-l3-real-speaker-count/clip.wav](assets/audio/speakers/speakers-l3-real-speaker-count/clip.wav) · 11.51s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio consists of three different adult male voices speaking in sequence, starting with a whisper, followed by a deep voice, and ending with a radio host.
- **Why the answer stands** The listener's report explicitly states that there are three distinct speakers in the recording, which directly supports option A.
- **Difficulty** score 0.3152 (auditor answered 5/5 blind, training solver 0.3333333333333333)


## Speakers & Dialogue — L4

### `speakers-l4-dialogue-turns`

- **Question** Count the speaker turns in this conversation (a turn ends whenever a different speaker starts talking). How many are there?
- **Answer** A. 2
- **Audio** [assets/audio/speakers/speakers-l4-dialogue-turns/clip.wav](assets/audio/speakers/speakers-l4-dialogue-turns/clip.wav) · 7.72s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** A female narrator introduces a quote from another woman who excitedly shouts about a race over the sound of a cheering crowd.
- **Why the answer stands** The report states there are two distinct speakers who each speak once and do not recur, which confirms there are exactly 2 speaker turns.
- **Difficulty** score 0.4233 (auditor answered 5/5 blind, training solver 0.0)

### `speakers-l4-speaker-gender`

- **Question** What kind of speaker is this?
- **Answer** C. an adult man
- **Audio** [assets/audio/speakers/speakers-l4-speaker-gender/clip.wav](assets/audio/speakers/speakers-l4-speaker-gender/clip.wav) · 4.9s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult man says 'The garden hose leaked near the connection point' while a plastic rustling sound is heard in the background.
- **Why the answer stands** The report explicitly and repeatedly states that the speaker is an adult man.
- **Difficulty** score 0.3817 (auditor answered 4/5 blind, training solver 0.75)

### `speakers-l4-dialogue-turns-real`

- **Question** How many turns are there in this dialogue? A turn is one uninterrupted stretch of speech by a single speaker; each speaker change starts a new turn.
- **Answer** B. 7
- **Audio** [assets/audio/speakers/speakers-l4-dialogue-turns-real/clip.wav](assets/audio/speakers/speakers-l4-dialogue-turns-real/clip.wav) · 23.05s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio is a compilation of short comedic dialogue clips from a television show, featuring multiple male and female speakers interspersed with audience laughter.
- **Why the answer stands** The report lists 7 distinct speech events and explicitly mentions 6 transitions between clips, which corresponds to 7 turns in total.
- **Difficulty** score 0.4002 (auditor answered 5/5 blind, training solver 0.25)

### `speakers-l4-speaker-count`

- **Question** How many speakers take part?
- **Answer** B. 1
- **Audio** [assets/audio/speakers/speakers-l4-speaker-count/clip.wav](assets/audio/speakers/speakers-l4-speaker-count/clip.wav) · 4.51s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult man speaks a single sentence in English with no background noise.
- **Why the answer stands** The listener's report explicitly states multiple times that there is only one speaker, which directly supports the claimed answer of 1.
- **Difficulty** score 0.3806 (auditor answered 5/5 blind, training solver 0.25)

### `speakers-l4-turn-order`

- **Question** Count how many times a different person takes over speaking.
- **Answer** C. 5
- **Audio** [assets/audio/speakers/speakers-l4-turn-order/clip.wav](assets/audio/speakers/speakers-l4-turn-order/clip.wav) · 32.74s · 7 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** Three people discuss conflicting weather forecasts and how it might affect their travel plans.
- **Why the answer stands** The report explicitly states that there are 5 speaker changes, which directly supports the claimed answer of 5 (Option C).
- **Difficulty** score 0.4166 (auditor answered 5/5 blind, training solver 0.16666666666666666)

### `speakers-l4-real-speaker-count`

- **Question** How many different speakers can be heard in this recording?
- **Answer** A. 3
- **Audio** [assets/audio/speakers/speakers-l4-real-speaker-count/clip.wav](assets/audio/speakers/speakers-l4-real-speaker-count/clip.wav) · 15.27s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The recording consists of three separate clips of different adult women speaking in English.
- **Why the answer stands** The listener's report explicitly states that there are three distinct speakers in the recording, which directly supports option A.
- **Difficulty** score 0.3965 (auditor answered 5/5 blind, training solver 0.16666666666666666)


## Speakers & Dialogue — L5

### `speakers-l5-dialogue-turns`

- **Question** In this exchange, how many speaking turns occur in total?
- **Answer** C. 2
- **Audio** [assets/audio/speakers/speakers-l5-dialogue-turns/clip.wav](assets/audio/speakers/speakers-l5-dialogue-turns/clip.wav) · 11.1s · 9 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult woman and an adult man take turns reading literary lines over a continuous background scraping sound.
- **Why the answer stands** The report explicitly states that there are 'two conversational turns' in the recording, which directly supports the claimed answer of 2.
- **Difficulty** score 0.5046 (auditor answered 2/5 blind, training solver 0.25)

### `speakers-l5-speaker-gender`

- **Question** Which best describes the voice you hear?
- **Answer** B. an adult woman
- **Audio** [assets/audio/speakers/speakers-l5-speaker-gender/clip.wav](assets/audio/speakers/speakers-l5-speaker-gender/clip.wav) · 5.12s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** An adult woman speaks a single sentence in English accompanied by a rapid clicking or tapping sound in the background.
- **Why the answer stands** The listener's report explicitly states multiple times that the speaker is an adult woman, which directly supports option B.
- **Difficulty** score 0.4818 (auditor answered 2/5 blind, training solver 0.75)

### `speakers-l5-speaker-count`

- **Question** How many distinct people speak in this recording?
- **Answer** B. 3
- **Audio** [assets/audio/speakers/speakers-l5-speaker-count/clip.wav](assets/audio/speakers/speakers-l5-speaker-count/clip.wav) · 27.87s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio features three different women speaking in Mandarin Chinese, with a brief coughing fit in the middle.
- **Why the answer stands** The listener's report explicitly states that there are 3 distinct speakers in the recording, which directly supports the claimed answer B.
- **Difficulty** score 0.4879 (auditor answered 0/5 blind, training solver 0.8333333333333334)

### `speakers-l5-dialogue-turns-real`

- **Question** In this real conversation, how many speaking turns occur in total?
- **Answer** A. 2
- **Audio** [assets/audio/speakers/speakers-l5-dialogue-turns-real/clip.wav](assets/audio/speakers/speakers-l5-dialogue-turns-real/clip.wav) · 4.27s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** The audio contains a calm male voice saying 'I wonder' followed by a dramatic, crying voice screaming 'Kids are talking by the door!'
- **Why the answer stands** The report states there are two distinct speakers who each speak once with one speaker change, which supports the claimed answer of 2 speaking turns.
- **Difficulty** score 0.4556 (auditor answered 5/5 blind, training solver 0.25)

### `speakers-l5-real-speaker-count`

- **Question** How many of the speakers are women?
- **Answer** A. 2
- **Audio** [assets/audio/speakers/speakers-l5-real-speaker-count/clip.wav](assets/audio/speakers/speakers-l5-real-speaker-count/clip.wav) · 40.61s · 6 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** This audio is a compilation of various short speech clips from seven different English-speaking adults, interspersed with brief moments of background music and laughter.
- **Why the answer stands** The report explicitly states that there are 2 adult women among the 7 distinct speakers, which directly supports option A.
- **Difficulty** score 0.5026 (auditor answered 4/5 blind, training solver 0.16666666666666666)

### `speakers-l5-dialogue-turns-2`

- **Question** How many turns are there in the dialogue? A turn is one uninterrupted speech by a single speaker. Each speaker change counts as one turn.
- **Answer** B. 2
- **Audio** [assets/audio/speakers/speakers-l5-dialogue-turns-2/clip.wav](assets/audio/speakers/speakers-l5-dialogue-turns-2/clip.wav) · 10.5s · 8 tools
- **Quality** pass A 5/5 (showcase), pass B 5/5 (showcase)
- **Heard, blind** Two women take turns reading sentences about construction, a river level, and a community garden.
- **Why the answer stands** The report states there is 1 speaker change from Speaker 1 to Speaker 2, which corresponds to exactly 2 turns of speech.
- **Difficulty** score 0.7162 (auditor answered 0/5 blind, training solver 0.0)
