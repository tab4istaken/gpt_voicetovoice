# gpt_voicetovoice

This is a simple Python script that integrates GPT models with a voice-in voice-out system, meaning it takes voice input and it outputs the GPT response using TTS.

## Installation

Simply clone the repository with Git, then install the PIP requirements.

```bash
  git clone https://github.com/tab4istaken/gpt_voicetovoice
  cd gpt_voicetovoice
  pip install -r requirements.txt
```

Within the script, make sure to add your own [OpenAI API key](https://platform.openai.com/api-keys), as well as the system prompt you want to use.

The script uses your system's default microphone for input. It can also detect the language you're speaking. **If you'd like GPT's response to have the right accent/pronunciation for your language, read the next section**.

## Add TTS support for other languages

Locate the following lines of code inside the script (should be around **line 46**):

```python
if language == "en":
    voice = "en-US-AriaNeural"
elif language == "ja":
    voice = "ja-JP-NanamiNeural"
else:
    voice = "en-US-AriaNeural"
```

As you can see, the script picks a TTS voice based on the language detected, defaulting to **English** for all languages that aren't handled. By default, **English** and **Japanese** are supported.

Firstly, as this script uses OpenAI's Whisper model for speech-to-text, make sure that your language is supported. You can see all languages Whisper supports [here](https://platform.openai.com/docs/guides/speech-to-text/supported-languages).

Next, using [this list](https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462), locate your desired language and choose a voice. For most languages, there are multiple options for voices, usually with support for multiple accents. 

As an example, let's imagine we want to add **Romanian**. Here are the available voices in this case:

```bash
Name: Microsoft Server Speech Text to Speech Voice (ro-RO, AlinaNeural)
ShortName: ro-RO-AlinaNeural
Gender: Female
Locale: ro-RO
VoiceTag: {'ContentCategories': ['General'], 'VoicePersonalities': ['Friendly', 'Positive']}

Name: Microsoft Server Speech Text to Speech Voice (ro-RO, EmilNeural)
ShortName: ro-RO-EmilNeural
Gender: Male
Locale: ro-RO
VoiceTag: {'ContentCategories': ['General'], 'VoicePersonalities': ['Friendly', 'Positive']}
```

Let's pick the first one. Now, we need to pay attention to the **ShortName**, as that's what we'll be using in the script. In this case, that's **ro-RO-AlinaNeural**.

Following the same pattern in the script, we'll update it to support the chosen voice. Here's what it should look like after the new changes:

```python
if language == "en":
    voice = "en-US-AriaNeural"
elif language == "ja":
    voice = "ja-JP-NanamiNeural"
elif language == "ro":
    voice = "ro-RO-AlinaNeural"
else:
    voice = "en-US-AriaNeural"
```

If you'd like, you can also edit the already provided voices.

## Integrating with RVC

This script is also useful if you'd like to use [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/en/README.en.md) to clone someone's voice and use it for what GPT outputs. 

The fastest (and easiest) way to use RVC with this script is via a real-time RVC voice changer. For this example, I'll be using the [w-okada voice changer](https://github.com/w-okada/voice-changer/tree/master).

First, download [VB-CABLE](https://vb-audio.com/Cable/). We'll be using this software to create a virtual input source, which will help us redirect the TTS output of the script to the voice changer so that it can be changed into the RVC voice.

In the script, locate the following line (should be around **line 74**):

```python
#sd.default.device = 12
```

We'll need to identify the ID that belongs to the VB-CABLE Input. Run Python in a terminal and import the **sounddevice** library.

```python
>> import sounddevice as sd
```

Next, list the sound devices.

```python
>> print(sd.query_devices())
```

You should get a list of sound devices. Locate the VB-CABLE Input. It should look something like this:

```bash
14 CABLE Input (VB-Audio Virtual C, MME (0 in, 2 out)
```

The number at the beginning represents the ID of the device (in my case, 14). In the script, uncomment the line mentioned earlier and change "12" to the ID you found. In my case, it'll look like this:

```python
sd.default.device = 14
```

Now, in the voice changer, make sure the **input** is set to the **VB-CABLE Output**. Leave the **output** as your normal sound output. For the w-okada voice changer, it'll look something like this:

![](https://i.imgur.com/GktvTrD.png)

After that, simply start the voice changer and run the script. If you did everything correctly, you should only hear the RVC voice when GPT replies. If the voice sounds a little off, you can tweak the TUNE (pitch) setting until it sounds right.
