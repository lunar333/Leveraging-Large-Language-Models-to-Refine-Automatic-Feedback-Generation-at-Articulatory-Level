import json
import openai
import os
import logging
#logging.setLevel(logging.WARNING)
class GenerateText:
    proxy = None
    model = ''
    message_list = []
    def __init__(self) -> None:
        with open('./config.json', 'r', encoding='utf-8') as inform:
            config = json.load(inform)
            openai.api_key = config["api-key"]
            self.model = config["model"]
            self.message_list.append({"role": "user", "content" : "请以后都使用中文回答我的问题"})
            self.message_list.append({"role": "assistant", "content" : "好的，以后我都会使用中文回答"})
            self.message_list.append({"role": "user", "content" : "有一个八维的发音属性向量，每一维向量代表口型的位置数据，如第一维度，代表jaw（下巴）的位置，使用数字表示所处的位置：0:Nearly Closed：1:Neutral, 2:Slightly Lowered，如第一维度是0，表示jaw(下巴）近乎关闭，以此类推。第二维度lip separation：0:Closed, 1: Slightly Apart, 2:Apart, 3:Wide Apart。 第三维度lip rounding： 0:Rounded, 1:Slightly Rounded,  2:Neutral,  3:Spread。 第四维度tongue frontness: 0:Back, 1:Slightly Back, 2:Neutral, 3:Slightly Front。第五维度tongue height：0:Low, 1:Mid, 2:Mid-High, 3:High。第六维度tongue tip: 0:low, 1: mid, 2: mid-High 3: High 第七维度velum：0:Closed, 1:Open。第八维度voicing，0:Unvoiced, 1:Voiced。现在需要你依据语音学和生理学的知识，通过计算两个发音属性向量（一个为正确的发音属性向量，一个为实际说话时的发音属性向量）的相似度，来判断说话人是否有发音错误，如果有请给出原因和建议。例如发IPA phone b时，正确发音属性向量为（1，0，2，2，1，1，0，1）或（1，2，2，2，1，1，0，1），说话人发音属性向量为（1，0，2，2，1，1，0，0），要求你通过计算发音向量的相似度，并通过一些语音学和生理学的知识判断该说话人是否发音错误，并给出理由"})
            self.message_list.append({"role": "assistant", "content" : "们可以通过计算向量的相似度（例如使用欧几里得距离或余弦相似度）来量化发音的偏差。对于给出的例子：正确的发音属性向量为（1，0，2，2，1，1，0，1）或（1，2，2，2，1，1，0，1），说话人的发音属性向量为（1，0，2，2，1，1，0，0）。我们可以通过比较这两个向量来判断发音的准确性。在这个例子中，最后一维（代表发音是否有声）在正确的发音和说话人的发音中有差异。在正确的发音中，最后一维应为1（有声），而在说话人的发音中，最后一维为0（无声）。因此，我们可以得出结论，说话人在发IPA phone b 时发音错误，错误出在发音的有声性上。b 应该是一个有声的辅音，但说话人发出的是无声的。建议说话人专注于在发出 b 音时确保声带振动"})
            self.message_list.append({"role": "user", "content" : "音素转发音属性的关系如下：sh 22133000，iy 01343001 ，hh 22221100，ae 33230001，d  11243401， 12242301，y  12243301，er 22221001，aa 32110001，r  12122301，k  12203100 ，12202100，s  12233300，uw 11013001，t  112434001， 2242300，ih 32342001，n  11223411，g  12203101 ，12202101，w  12003101，ao 32102001，dh 22242201，l  12232401，ow 32132001 ，21012001，m  10221111，eh 32231001，oy 22101001 ，12332001，ay 32220001， 12332001，b  10221101， 12221101，v  20221101，f  20221100，z  12233301，th 22242200，ah 22220001，p  10221100 ，12221100 ，ey 12342001，ng 12203111，ch 22243400， 12133000，uh 12112001，zh 22133001，jh 22243401， 12133001，aw 32220001， 12012001。请你记住这张映射表，每个音素对应8个数字（8维发音属性向量），或者16个数字（两个8维发音属性向量）。问题：跟读文本：but there came no promise from the bow of the canoe，对应的正确的音素为sil b ah t dh eh r k ey m n ow p r aa m ah s f r ah m dh ah b ow ah v dh ah k ah n uw sil，实际发音音素为：sil b ah sil dh eh r k eh m n ao p w aa m ah s f r ah n dh ah b ao ah v dh ah k ah n uw sil，请你将正确音素和实际音素通过音素转发音属性表转换，转换完之后，将两个音素进行分词，对应到跟读文本的每个单词，对比发音属性的不同，并且你现在需要作为一个英语老师，运用你的教学经验给出专业的反馈，并且你需要结合每个单词发音属性分析的结果，但在给出反馈时候，可以不用给出发音属性转换的过程。请给出最主要的错误，如替换，删除，插入这几类错误。"})
            self.message_list.append({"role": "assistant", "content" : "首先，我们将音素转换为发音属性向量：正确的发音属性向量：b: 10221101, ah: 22220001, t: 112434001,dh: 22242201, eh: 32231001, r: 12122301,k: 12203100, ey: 12342001, m: 10221111,n: 11223411, ow: 32132001, p: 10221100,r: 12122301, aa: 32110001, m: 10221111,ah: 22220001, s: 12233300, f: 20221100,r: 12122301, ah: 22220001, m: 10221111,dh: 22242201, ah: 22220001, b: 10221101,ow: 32132001, ah: 22220001, v: 20221101,dh: 22242201, ah: 22220001, k: 12203100,ah: 22220001, n: 11223411, uw: 11013001。实际的发音属性向量：b: 10221101, ah: 22220001, sil: n/a,dh: 22242201, eh: 32231001, r: 12122301,k: 12203100, eh: 32231001, m: 10221111,n: 11223411, ao: 32102001, p: 10221100,w: 12003101, aa: 32110001, m: 10221111,ah: 22220001, s: 12233300, f: 20221100,r: 12122301, ah: 22220001, n: 11223411,dh: 22242201, ah: 22220001, b: 10221101,ao: 32102001, ah: 22220001, v: 20221101,dh: 22242201, ah: 22220001, k: 12203100,ah: 22220001, n: 11223411, uw: 11013001。通过对比每个单词对应的发音属性向量，如but: 正确发音音素为[b ah t]，实际发音音素为[b ah sil]，发音属性向量完全不匹配，'t'被错误地替换为了静音。最后，我们总结出的错误有：替换错误：在这个句子的发音中，有多处音素替换错误。例如，在 came 的发音中，元音音素 ey 被替换为了 eh。在 promise中，音素 r 被替换为了 w。最后，在 from 中，音素 m 被替换为了 n。为改进这个问题，你需要更多地练习并熟悉每个音素的发音，尤其是元音音素。元音音素在英语中很重要，并且有时候会比较微妙，所以要加以注意。插入错误：在这个句子中没有出现插入错误。插入错误是指在发音中错误地添加了不必要的音素。删除错误：在 but 的发音中，音素 t 被删除了，变成了静音。这可能是由于未能清晰地发出词尾的音。对于这个问题，建议练习清晰发音每个音素，尤其是在词尾。舌位位置错误：这个问题在这个句子中并没有明显出现。舌位位置错误是指在发音过程中，舌头的位置放错了，导致音素发音不准确。如果有舌位位置错误的话，可能需要找专业的发音教练或语言治疗师来辅导，通过专业的训练来纠正。"})
            self.message_list.append({"role": "user", "content" : "上面回复中，反馈再具体并且专业一些，比如音素 m 被替换为了 n，[m] & [n]都是鼻辅音[m]叫做双唇鼻辅音，发音时双唇要始终保持紧闭状态，舌头放平，自然放松，让气流从鼻腔中送出；[n]叫做舌尖齿龈鼻辅音，发音时双唇始终微微张开，舌尖上扬轻轻抵住上齿龈，让气流从鼻腔送出，二者的最大区别是嘴巴是否张开，舌头的摆放位置。而不要回复“你需要更多地练习并熟悉每个音素的发音，尤其是元音音素。元音音素在英语中很重要，并且有时候会比较微妙，所以要加以注意。”因为这是正确，但是毫无信息量的信息，给不了练习者太多有用信息。请重新回复刚才的问题，请发挥你作为英语老师的教学经验，以及从发音属性对比中得到的信息"})
            self.message_list.append({"role": "assistant", "content" : "了解了你的需求，接下来我将对上述错误进行更专业的反馈：替换错误：在这个句子的发音中，有多处音素替换错误。在 came 的发音中，元音音素 ey 被替换为了 eh。这可能是因为舌头的位置太低，没有做到像 ey 那样中心和前部元音的位置。ey 发音时，口型应略开，舌尖下降，舌后部稍微上升。你可以通过观察自己的口腔和舌头的动作，以及听听标准的 ey 发音，加强这个音素的练习。在 no和 bow 中，元音 ow 被替换为了 ao。ow 的发音应当从圆唇中元音开始，然后向后降低舌头位置到低元音。而 ao 的发音舌头位置一直在后部的位置，这可能是因为你在发 ow 的时候没有做出这种向后移动的动作。在 promise 中，音素 r 被替换为了 w。这可能是因为你在发 r 的时候舌尖没有卷起来，这是英语 r 音的特点。最后，在 from 中，音素 m 被替换为了 n。这可能是因为你在发 m 的时候没有完全闭合嘴唇，导致声音从口腔而非鼻腔出来。m 音的发音需要嘴唇完全闭合，而 n 音的发音需要舌尖抵住上齿龈。插入错误：在这个句子中没有出现插入错误。删除错误：在 but 的发音中，音素 t 被删除了。这可能是由于你在发 t 的时候舌尖没有抵住上齿龈，或者没有用足够的力气去爆破。t 音的发音需要舌尖抵住上齿龈，然后用力爆破。我希望这些具体的反馈可以帮助你更好地理解和改善你的发音。请你继续坚持练习，如果有任何问题，随时向我询问。"})        
            self.message_list.append({"role": "user", "content" : "非常好！请以后就按照这个回复模块进行回复。跟读文本：he looked like one who had passed through an uncomfortable hour or two。正确音素：hh iy l uh k t sil l ay k sil w ah n hh uw hh ae d sil p ae s t th r uw ae n ah n k ah m f er t ah b ah l aw r ao r t uw sil。实际音素：hh iy l uh k t z sil l ay k sil w ah n hh uw hh ae d sil p aa s t s r uw ae n ah n k ah m f er t ah b ah ow aw r aa r t uw sil。请按照模版进行回复，不要回复之前正确，但是没有信息量，给不了练习者太多有用信息的回复"})
            self.message_list.append({"role": "assistant", "content" : "了解你的需求，以下是对你提供的实际发音音素与正确音素的对比分析与建议：替换错误：passed中的音素 ae 被替换为了 aa。这可能是因为舌头在发音时的位置偏低。当发 ae 音时，舌头应位于口腔的前部并稍稍抬高，而 aa 音的舌位较低。你可以多练习 ae 音，观察口腔形状和舌位，熟悉这个音素的发音特点。在 or 的发音中，元音音素 ao 被替换为了 aa。这可能是舌尖的位置没有移到像 ao 那样的中央，而是像 aa 那样保持在前面。ao 音需要舌尖稍微后移，而 aa 则舌尖在前。建议多加练习，注意舌尖的位置。插入错误：在 looked 和 passed 中，音素 z 和 s 被错误地插入了。这可能是你在发 k 和 t 的时候没有清晰地爆破，而产生了摩擦音。记住 k 和 t 都是爆破音，需要舌尖或舌后抵住上颚，然后用力爆破。删除错误：在 through的发音中，音素 th 被删除了。这可能是因为你在发 th 的时候舌尖没有伸到牙齿之间，或者没有足够的呼气形成这个摩擦音。记住 th 音需要舌尖位于上下牙齿之间，并向外稍微吹气。"})   
            self.message_list.append({"role": "user", "content" :'''我会按照你要求的模板对正确音素和实际音素进行分词,并找出每个单词对应的音素,然后通过对比每个单词的音素,找到其中存在的替换、删除、插入错误。

            正确音素序列: 实际音素序列: 对比结果:
            for: [f ao r] - for: [f ao r] - 无误
            the: [dh ah t] - the: [dh ah t] - 无误
            twentieth: [w eh n t iy ih th] - twentieth: [w eh n t iy ih th] - 无误
            time: [t ay m] - time: [t ay m] - 无误
            that: [dh ae t] - that: [dh ae t] - 无误
            evening: [iy v n ih ng] - evening: [iy v n ih ng k] - 删除错误,"k" 被删除,替换错误,"k" 被替换为 "k"
            the: [dh ah] - the: [dh ah] - 无误
            two: [t uw] - two: [t uw] - 无误
            men: [m eh n] - men: [m eh n] - 无误
            shook: [sh uh k] - shook: [sh uh k] - 无误
            hands: [hh ae n d z] - hands: [hh ae n s s] - 替换错误,"d z" 被替换为 "s s"

            通过分析音素序列,我们发现了替换、删除和插入错误。在这个例子中,错误发生在 "twentieth" 单词中,"k" 被删除,"k" 被替换为 "k" 和 "d z" 被替换为 "s s"。这些错误可能是由于发音不清或快速发音导致的。

            请你根据上面分词对比分析的结果，将每个音素转换对应到发音属性，同时你需要发挥你作为英语老师的教学经验结合发音属性对比得到的信息，给出最合理，符合语音学现象，可解释的错误，并且给出能够给予二语学习者有切实帮助，有信息量的反馈'''})
            self.message_list.append({"role": "assistant", "content" : '''在这个例子中，我们发现了一些发音上的替换和删除错误。以下是具体的反馈：
                                      
            替换错误：在单词 "hands" 中，末尾的音素 "d z" 被替换为 "s s"。在音素属性上，"d z" 是一个舌尖齿龈浊辅音，它的发音需要舌尖接触上齿龈，同时声带振动。而 "s s" 是一个舌尖齿龈清辅音，虽然舌尖的位置类似，但声带并不振动。这个替换错误可能会导致听者理解为一个不同的单词。建议你注意这两种音素的发音差异，尤其是在清、浊辅音之间。
            删除错误：在单词 "evening" 中，末尾的音素 "k" 被删除了。在音素属性上，"k" 是一个舌尖软腭塞音，这意味着发音时舌尖接触软腭，气流在口腔内被完全阻塞，然后突然释放。这个删除错误可能会导致听者理解为一个不同的单词或词形。建议你在发音这类音素时，尤其注意口腔内的气流管理和舌尖的位置。

            替换错误：在单词 "evening" 中，音素 "ng" 被替换为 "nk"。在音素属性上，"ng" 是一个鼻音，发音时舌尖升起接触软腭，同时声带振动并且气流通过鼻腔。而 "nk" 是一个舌尖软腭塞音，虽然舌尖的位置类似，但是气流不通过鼻腔，而是在口腔内被完全阻塞，然后突然释放。这种替换可能会改变单词的发音，从而影响听者的理解。建议你注意这两种音素的发音差异，尤其是鼻音和塞音之间。

            总的来说，注意清、浊辅音的区别，注意塞音的发音，以及鼻音和塞音的区别，这将有助于你更准确地发音这些音素。记住，良好的发音习惯需要时间和练习来建立，不要灰心，持续的练习会带来改进。祝你学习进步！'''})   
    def getPrompt(self, message_list) -> str:
        completion = openai.ChatCompletion.create(
        model=self.model, 
        messages=message_list
        )
        return completion['choices'][0]['message']['content'].strip()
    def getText(self, text : str,text2: str) -> str:
        current_message_list = self.message_list.copy()
        current_message_list.append({"role": "user", "content": text})
        result = ''
        try:
            result = self.getPrompt(current_message_list)
            text_dict = {"content": text2, "summary" : result}
            with open('l2_fankui.json', 'a', encoding='utf-8') as json_file:
                json.dump(text_dict, json_file, ensure_ascii=False)
                json_file.write('\n')  # Write a newline to prepare for the next record
        except:
            logging.error('interaction with chatgpt error!!')
        return result


if __name__ == '__main__':
    gt = GenerateText()

    with open('./l2_fenci.json', 'r') as file: #please replace the path to spd-dataset-generate1.py generates path
        lines = file.readlines()
        # Process each line (which is a separate JSON object)
        for line in lines:
            data = json.loads(line.strip())  # convert the JSON data into a Python dictionary
            summary = data.get('summary')  # get the summary field
            text = summary +'\n\n'+'请你根据上面分词对比分析的结果，将每个音素转换对应到发音属性，同时你需要发挥你作为英语老师的教学经验结合发音属性对比得到的信息，给出最合理，符合语音学现象，可解释的错误，并且给出能够给予二语学习者有切实帮助，有信息量的反馈。你不需要告诉我发音属性的相关信息，只需要告诉我通过发音属性对比和其他知识得到的反馈即可，严格按照上一个问题回答的模版进行回答'
            text2 = summary +'\n\n'+'请你根据上面分词对比分析的结果，将每个音素转换对应到发音属性，同时你需要发挥你作为英语老师的教学经验结合发音属性对比得到的信息，给出最合理，符合语音学现象，可解释的错误，并且给出能够给予二语学习者有切实帮助，有信息量的反馈'
            result =  gt.getText(text,text2)
