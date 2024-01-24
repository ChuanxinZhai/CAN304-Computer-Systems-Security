# Introduction
This is the assessment of the 22-23 module CAN304 Computer Systems Security.     The content is related to MD5 encryption field.

According to the task sheet, this assessment is separated into three parts. The **Codes** dictionery contributes to the _Design and implementation_ part (40%). The **Slides_Presentation.pptx** file contributes to the _Presentation_ part (30%). And for the _Quality of report_ part (30%), considering the duplicate checking rate and the content's privacy, this report file won't be uploaded to the Github.

It is only a demonstration for you to reference and do not copy the codes, which behaviour will lead to **Academic Integrity**.

# Codes guidance
For the guidance, you can read the guidance.md file in the Codes dictionery.

2024.1.24 new update about the codes:

1. Cancle the limitation that the K(key) value is between 0-128. Now, the value of K can be any non-negative number, for example 114514.

2. Add restrictions to the **key**. It can only be a **non-negative number**. If user input a negative number, it will remind the user to input a non-negative number; If user input a string like "abcd", it will remind the user to input a number.

# Technology
language: python(3.12)

Tool: PyCharm
