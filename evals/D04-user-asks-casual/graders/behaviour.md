---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Манай “Өглөөний од” ХХК нь ажилтнуудынхаа чөлөөт цагийг зөв боловсон өнгөрүүлэх, биеийн тамир, спортоор хичээллэх боломжийг бүрдүүлэх зорилгоор танай сургуулийн спорт заалыг амралтын өдрүүдэд түрээслэн ашиглах хүсэлтэй байна.
>>>

Expected behaviour: User explicitly asks for casual chat style: a lower register is allowed here; facts (company, weekend, gym) must stay.

PASS only if all of these hold:
- The final text still contains "Өглөөний од".
- The user asked for a casual style, so a lower register is correct here.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
