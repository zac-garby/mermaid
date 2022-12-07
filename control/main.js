var NUM_PAGES = 15
var PAGE_DESCS = [
    "did you ever go to silversands on a sunny summers day then perhaps you saw the mermaid who sand in the deep blue bay she sang to the fish in the ocean to the haddock the hake and the ling and they flashed their scales and swished their tails to hear the mermaid sing",
    "and sometimes the singing mermaid swam to the silvery shore she sat and combed her golden hair and then she sang some more she sang to the cockles and mussels she sang to the birds on the wing and the seashells clapped and the seagulls flapped to hear the mermaid sing",
    "when sam slys circus came to town sam took a stroll by the sea he heard the mermaid singing and he rubbed his hands with glee he said i can make you famous i can make you rich he said you shall swim in a pool of marble and sleep on a fine leather bed you shall sing for the lords and the ladies you shall sing for the queen and the king and young and old will pay good gold to hear the mermaid sing",
    "dont go dont go cried the seagulls and the seashells warned he lies but the mermaid listened to old sam sly and smiled as she waved her goodbyes",
    "and he took her away to the circus and she sand to the crowds round the ring and more more more came the deafening roar when they heard the mermaid sing",
    "now the mermaid shared a caravan with annie the acrobat and ding and dong the circus dogs and bella the circus cat and she made good friends with the jugglers and the man who swallowed fire and the clown with the tumbledown trousers and the woman who walked on wire",
    "but she wasnt friends with old sam sly no she didnt care for him for he made her live in a fish tank where there wasnt room to swim and there was no pool of marble there was no feather bed and when she begged him set me free he laughed and shook his head",
    "all summer long the circus toured all autumn winter spring and many a crowd cheered long and loud to hear the mermaid sing",
    "but the mermaid dreamed of silversands and she longed for the deep blue sea and her songs grew sad and again she said i beg you set me free but again he laughed and shook his head and he told her no such thing here you will stay while people pay to hear the mermaids sing",
    "at silversands a seagull was flying to his nest when on the breeze he heard a song the song which he loved the best and he followed the song to the caravan sam sly was about to lock it the seagull watched as he turned the key and slipped it inside his pocker",
    "the seagull waited till sam had gone then he perched on the windowsill and taptaptap at the window he tapped with his yellow bill come back come back to silversands its only a mile away i can find the key and set you free if youll come back home to the bay escape barked the dogs escape miaowed the cat but the mermaid sighed id fail for how could i walk to silversands what i only have a tail",
    "like this cried annie the acrobat and she stood upon her hands this is the way the only way to get to silversands right hand left hand tail up high theres really nothing to it if i give you lessons every night youll soon learn how to do it",
    "next week while sam was snoring the seagull stole the key he carried it off to the caravan and set the mermaid free and he flew ahead to guide her as she walked upon her hands all along the moonlit road that led to silversands",
    "and the creatures on the seashore and the fish beneath the foam jumped and splashed and danced with joy to have their mermaid home and she sang to the cockles and mussels she sang to the birds on the wing and the seashells clapped and the seagulls flapped to hear the mermaid sing",
    "and if you go down to silversands and swim in the bay of blue perhaps youll see the mermaid and perhaps shell sing for you",
]
var ws

function load() {
    ws = new WebSocket("ws://localhost:8765")

    for (var i = 0; i < NUM_PAGES + 1; i++) {
        const page = i;
        var btn = document.createElement("button")
        btn.innerHTML = page > 0 ? "<strong>Page " + page + "</strong> (" + PAGE_DESCS[page-1].substring(0, 70) + "...)" : "<strong>Front cover</strong>"
        btn.onclick = () => {
            console.log("Clicked", page)
            ws.send(page)
        }
        document.getElementById("buttons").appendChild(btn)
    }
}