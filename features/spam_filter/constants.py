import re

EXPLICIT_KEYWORDS = {
    "english": [
        "nude", "sex chat", "video call", "vc", "escort", "call girl",
        "dating", "hot", "sexy", "adult", "xxx", "porn",
        "nsfw", "hookup", "earning",
        "investment", "money", "paid", "available now"
    ],
    "hindi": [
        "नंबर लेना", "आंटी", "भाभी", "सर्विस", "कॉल करो",
        "मैसेज करो", "पैसे कमाओ", "फ्री", "लड़की", "मिलो"
    ],
    "tamil": [
        "பெண்", "சேவை", "கால்", "பணம்", "இலவசம்"
    ],
    "patterns": [
        re.compile(r"(.)\1{5,}"),  # repeated chars
        re.compile(r"http[s]?://"),
        re.compile(r"@\w+"),
    ]
}

SEVERE_KEYWORDS = [
    "child", "minor", "underage", "kid", "cp",
    "school girl", "college girl", "young girl",
    "बच्चा", "नाबालिग", "குழந்தை"
]