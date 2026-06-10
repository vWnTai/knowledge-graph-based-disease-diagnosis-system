# 📊 Báo Cáo Đánh Giá Hệ Thống GraphRAG

**Ngày đánh giá:** 10/06/2026 10:35
**Model AI:** gemma3
**Số test cases:** 25

---

## 1. Kết Quả Đánh Giá Thủ Công

| Metric | Giá trị |
|--------|--------|
| KG Accuracy | 19/25 (76.0%) |
| AI Response Rate | 100.0% |
| Avg KG Confidence | 99.0% |
| Avg Response Time | 4.1s |

### Phân Tích Theo Nhóm Bệnh

| Nhóm | Đúng/Tổng | Accuracy |
|------|-----------|----------|
| D | 6/7 | 86% |
| I | 3/5 | 60% |
| J | 3/4 | 75% |
| K | 6/6 | 100% |
| X | 1/3 | 33% |

## 2. Kết Quả RAGAS

| Metric | Score |
|--------|-------|
| Raw Results | {'faithfulness': 0.6609, 'answer_relevancy': nan, 'llm_context_precision_without_reference': 0.9583, 'context_recall': 0.9130} |

## 3. Chi Tiết Từng Test Case

### TC01 [J] ✅

- **Câu hỏi:** Tôi bị sốt cao đột ngột, đau mỏi cơ khớp, đau đầu, hắt hơi sổ mũi và ho khan. Tôi có thể bị bệnh gì?
- **Expected:** J09
- **KG Result:** J09 (confidence: 95.0%)
- **AI Time:** 4.7s
- **AI Answer:** Chào bạn, với các triệu chứng bạn mô tả như sốt cao đột ngột, đau mỏi cơ khớp, đau đầu, ho khan, kết quả phân tích của chúng tôi cho thấy khả năng cao nhất là **cúm do virus (J09)** với độ tin cậy 95%. 

Tuy nhiên, vẫn có khả năng bạn bị cúm kèm viêm phổi hoặc cúm với các biểu hiện hô hấp khác. Chún...

### TC02 [J] ✅

- **Câu hỏi:** Bệnh nhân ho kèm đờm đục, sốt cao run rẩy, đau ngực khi hít thở sâu và khó thở. Chẩn đoán có thể là gì?
- **Expected:** J18.0
- **KG Result:** J18.0 (confidence: 95.0%)
- **AI Time:** 5.6s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn mô tả (ho kèm đờm đục, sốt cao run rẩy, đau ngực khi hít thở sâu và khó thở), bệnh có khả năng cao nhất là **Viêm phế quản phổi (ICD-10: J18.0) với độ tin cậy 95.00%**.

Chúng tôi cũng cần loại trừ các khả năng khác như Viêm phổi do E. coli, Klebsiella pneumoni...

### TC03 [J] ✅

- **Câu hỏi:** Tôi bị khó thở tiến triển, ho khan kéo dài, giảm khả năng gắng sức và đau tức ngực. Bệnh này là gì?
- **Expected:** J61
- **KG Result:** J61 (confidence: 100.0%)
- **AI Time:** 5.4s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng của bạn như khó thở tiến triển, ho khan kéo dài, giảm khả năng gắng sức và đau tức ngực, kết quả phân tích đồ thị tri thức y khoa cho thấy khả năng cao nhất là bạn bị **bệnh bụi phổi amian và các sợi khóang khác (J61)**. Các triệu chứng này cũng có thể liên quan đế...

### TC04 [I] ✅

- **Câu hỏi:** Bệnh nhân đau đầu dữ dội đột ngột, nôn vọt, cứng gáy và rối loạn ý thức. Đây có phải xuất huyết não không?
- **Expected:** I60
- **KG Result:** I60 (confidence: 100.0%)
- **AI Time:** 4.0s
- **AI Answer:** Chào bạn, với các triệu chứng đau đầu dữ dội đột ngột, nôn vọt, cứng gáy và rối loạn ý thức của bạn, theo phân tích từ đồ thị tri thức y khoa, **có khả năng cao bạn đang bị xuất huyết dưới màng nhện**.  Độ tin cậy của chẩn đoán này là 100%. Chúng ta sẽ cần làm thêm các xét nghiệm để xác định vị trí ...

### TC05 [I] ✅

- **Câu hỏi:** Bệnh nhân bị liệt nửa người, méo miệng, nói khó và rối loạn ý thức đột ngột. Chẩn đoán gì?
- **Expected:** I64
- **KG Result:** I64 (confidence: 95.0%)
- **AI Time:** 4.2s
- **AI Answer:** Dựa trên thông tin hiện có, bệnh nhân có khả năng cao bị đột quỵ không xác định do xuất huyết hay nhồi máu (Tai biến mạch máu não - ICD-10: I64) với độ tin cậy 95.00%. Các triệu chứng liệt nửa người, méo miệng phù hợp với chẩn đoán này. Cần phải thăm khám và làm thêm các xét nghiệm để xác định nguyê...

### TC06 [I] ✅

- **Câu hỏi:** Tôi bị nhức đầu vùng chẩm, hoa mắt chóng mặt, mặt đỏ bừng và ù tai. Có phải tăng huyết áp không?
- **Expected:** I10
- **KG Result:** I10 (confidence: 100.0%)
- **AI Time:** 4.6s
- **AI Answer:** Chào bạn, các triệu chứng bạn mô tả như nhức đầu vùng chẩm, hoa mắt chóng mặt, mặt đỏ bừng và ù tai rất phù hợp với bệnh tăng huyết áp. Dựa trên phân tích của hệ thống, khả năng cao nhất bạn bị tăng huyết áp (ICD-10: I10) với độ tin cậy 100%. Chúng ta cần kiểm tra huyết áp để xác định mức độ và có h...

### TC07 [K] ✅

- **Câu hỏi:** Bệnh nhân đau hố chậu phải dữ dội, sốt nhẹ và buồn nôn. Có phải viêm ruột thừa không?
- **Expected:** K35
- **KG Result:** K35 (confidence: 100.0%)
- **AI Time:** 3.8s
- **AI Answer:** Chào bạn, với các triệu chứng đau hố chậu phải dữ dội, sốt nhẹ và buồn nôn, kết quả phân tích đồ thị tri thức y khoa cho thấy khả năng cao nhất là bạn đang bị viêm ruột thừa cấp (ICD-10: K35).  Viêm ruột thừa là một tình trạng cần được thăm khám và chẩn đoán xác định bởi bác sĩ. Bạn nên đến khám nga...

### TC08 [K] ✅

- **Câu hỏi:** Tôi bị đau hạ sườn phải, vàng da và buồn nôn. Bệnh gì vậy?
- **Expected:** K82.0
- **KG Result:** K82.0 (confidence: 100.0%)
- **AI Time:** 3.4s
- **AI Answer:** Chào bạn, với các triệu chứng đau hạ sườn phải, vàng da và buồn nôn của bạn, hệ thống phân tích cho thấy khả năng cao nhất là tắc túi mật (ICD-10: K82.0). Các triệu chứng này cũng phù hợp với tình trạng sỏi mật. Chúng tôi sẽ cần làm thêm các xét nghiệm để xác định chính xác nguyên nhân và đưa ra phư...

### TC09 [K] ✅

- **Câu hỏi:** Bệnh nhân đau thượng vị, khó tiêu và buồn nôn. Chẩn đoán là gì?
- **Expected:** K29.1
- **KG Result:** K29.1 (confidence: 100.0%)
- **AI Time:** 2.8s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng đau thượng vị, khó tiêu và buồn nôn của bạn, kết quả phân tích đồ thị tri thức y khoa cho thấy khả năng cao nhất là **Viêm dạ dày cấp (ICD-10: K29.1)** với độ tin cậy 100%....

### TC10 [K] ✅

- **Câu hỏi:** Tôi bị tiêu phân có máu, đau bụng và tiêu chảy kéo dài. Bệnh gì?
- **Expected:** K51
- **KG Result:** K51 (confidence: 100.0%)
- **AI Time:** 4.1s
- **AI Answer:** Chào bạn, với các triệu chứng bạn mô tả như tiêu phân có máu, đau bụng và tiêu chảy kéo dài, hệ thống phân tích cho thấy bạn có khả năng cao bị **Viêm loét đại tràng chảy máu** (ICD-10: K51). Tình trạng này thường gây đau bụng, tiêu chảy và có máu trong phân.

Để xác định chính xác và có phương pháp...

### TC11 [K] ✅

- **Câu hỏi:** Bệnh nhân đau hạ sườn phải, sốt cao và buồn nôn. Có phải viêm túi mật?
- **Expected:** K80.0
- **KG Result:** K80.0 (confidence: 100.0%)
- **AI Time:** 3.4s
- **AI Answer:** Chào bạn, dựa trên thông tin hiện tại, khả năng cao nhất bạn đang bị sỏi túi mật có viêm túi mật cấp (Mã bệnh ICD-10: K80.0). Các triệu chứng đau hạ sườn phải, sốt cao và buồn nôn đều phù hợp với tình trạng này. Tuy nhiên, để xác định chính xác, cần phải thăm khám và làm thêm các xét nghiệm khác....

### TC12 [D] ✅

- **Câu hỏi:** Tôi bị da xanh xao, mệt mỏi hoa mắt chóng mặt, móng tay khô dễ gãy và nhịp tim nhanh khi gắng sức. Thiếu máu phải không?
- **Expected:** D50.1
- **KG Result:** D50.1 (confidence: 100.0%)
- **AI Time:** 2.7s
- **AI Answer:** Chào bạn, triệu chứng của bạn rất phù hợp với khả năng thiếu máu. Dựa trên phân tích, khả năng cao nhất là bạn bị chứng khó nuốt do thiếu sắt (D50.1). Chúng ta cần làm thêm các xét nghiệm để xác định chính xác loại thiếu máu và nguyên nhân gây ra nhé....

### TC13 [D] ✅

- **Câu hỏi:** Bệnh nhân da xanh xao, vàng da vàng mắt, nước tiểu sẫm màu và lách to. Đây là bệnh gì?
- **Expected:** D56
- **KG Result:** D56 (confidence: 100.0%)
- **AI Time:** 4.4s
- **AI Answer:** Chào bạn, dựa trên những triệu chứng bạn mô tả như da xanh xao, vàng da vàng mắt, nước tiểu sẫm màu và lách to, kết quả phân tích đồ thị tri thức cho thấy khả năng cao nhất là bạn bị Bệnh Thalassemia (mã ICD-10: D56). Các triệu chứng này rất đặc trưng cho bệnh Thalassemia và Alpha, Beta, cũng như Bệ...

### TC14 [D] ✅

- **Câu hỏi:** Tôi bị chấm nốt xuất huyết dưới da, chảy máu chân răng mũi, xuất huyết tiêu hóa và thời gian chảy máu kéo dài. Bệnh gì?
- **Expected:** D69
- **KG Result:** D69 (confidence: 100.0%)
- **AI Time:** 4.4s
- **AI Answer:** Chào bạn, với các triệu chứng bạn mô tả như chấm nốt xuất huyết dưới da, chảy máu chân răng mũi, xuất huyết tiêu hóa và thời gian chảy máu kéo dài, hệ thống phân tích cho thấy khả năng cao nhất bạn đang bị **Ban xuất huyết và các tình trạng xuất huyết khác (D69)**. Các triệu chứng của bạn khớp hoàn ...

### TC15 [D] ❌

- **Câu hỏi:** Bệnh nhân bị nhiễm trùng tái phát liên tục, sốt cao dai dẳng, loét niêm mạc miệng và hạch ngoại vi sưng to. Chẩn đoán gì?
- **Expected:** D84
- **KG Result:** D86 (confidence: 100.0%)
- **AI Time:** 2.3s
- **AI Answer:** Dựa trên các triệu chứng của bệnh nhân, chẩn đoán có khả năng cao nhất là **Bệnh sarcoid (Mã bệnh ICD-10: D86)**, với độ tin cậy 100%....

### TC16 [D] ✅

- **Câu hỏi:** Bệnh nhân nữ bị ra khí hư bất bất thường, chảy máu âm đạo bất thường, đau vùng hạ vị và kinh nguyệt không đều. Có phải ung thư cổ tử cung?
- **Expected:** D06
- **KG Result:** D06 (confidence: 100.0%)
- **AI Time:** 4.1s
- **AI Answer:** Chào bạn, với các triệu chứng bạn đang gặp phải như ra khí hư bất thường, chảy máu âm đạo bất thường, đau vùng hạ vị và kinh nguyệt không đều, theo phân tích từ hệ thống đồ thị tri thức, khả năng cao nhất là bạn bị Ung thư biểu mô tại chỗ của cổ tử cung (D06). Chúng tôi cần tiến hành thăm khám và cá...

### TC17 [X] ❌

- **Câu hỏi:** Bệnh nhân bị buồn nôn, nôn mửa, chóng mặt, đau bụng và co giật sau khi bị nhện cắn. Bệnh gì?
- **Expected:** X21
- **KG Result:** X41 (confidence: 100.0%)
- **AI Time:** 4.4s
- **AI Answer:** Dựa trên các triệu chứng của bệnh nhân (buồn nôn, nôn mửa, chóng mặt, đau bụng, co giật) và tiền sử có thể phơi nhiễm thuốc chống động kinh, an thần, bệnh nhân có khả năng cao bị **tai nạn ngộ độc do phơi nhiễm thuốc chống động kinh** (ICD-10: X41). Mặc dù bệnh nhân khai báo do bị nhện cắn, nhưng cá...

### TC18 [X] ✅

- **Câu hỏi:** Bệnh nhân buồn nôn, nôn mửa, chóng mặt, đau bụng và co giật sau khi uống rượu quá nhiều. Đây là gì?
- **Expected:** X45
- **KG Result:** X45 (confidence: 100.0%)
- **AI Time:** 3.5s
- **AI Answer:** Chào bạn, với các triệu chứng bạn mô tả như buồn nôn, nôn mửa, chóng mặt, đau bụng và co giật sau khi uống rượu quá nhiều, khả năng cao nhất là bạn bị **tai nạn ngộ độc và phơi nhiễm rượu (ICD-10: X45)**. Đây là một tình trạng nghiêm trọng cần được theo dõi và điều trị kịp thời.
...

### TC19 [I] ❌

- **Câu hỏi:** Bệnh nhân đau di chuyển các khớp lớn, có tiếng thổi ở tim, hồi hộp đánh trống ngực và khó thở nhẹ khi gắng sức. Bệnh gì?
- **Expected:** I08.9
- **KG Result:** I23.6 (confidence: 95.0%)
- **AI Time:** 5.7s
- **AI Answer:** Chào bạn, với các triệu chứng bạn mô tả như đau di chuyển các khớp lớn, tiếng thổi ở tim, hồi hộp đánh trống ngực và khó thở nhẹ khi gắng sức, kết quả phân tích đồ thị tri thức cho thấy khả năng cao nhất là bạn đang bị **biến chứng huyết khối trong buồng tim tâm nhĩ, tiểu nhĩ và tâm thất sau nhồi má...

### TC20 [J] ❌

- **Câu hỏi:** Trẻ em bị sốt nhẹ, chảy mũi, đau họng và ho. Có phải viêm đường hô hấp trên?
- **Expected:** J06.9
- **KG Result:** K35 (confidence: 95.0%)
- **AI Time:** 5.0s
- **AI Answer:** Chào bạn,

Với các triệu chứng sốt nhẹ, chảy mũi, đau họng và ho, theo phân tích đồ thị tri thức y khoa, viêm ruột thừa cấp có khả năng cao nhất (95.00%) là nguyên nhân chính. Mặc dù các triệu chứng này có thể xuất hiện trong viêm đường hô hấp trên, nhưng dựa trên thông tin hiện có, viêm ruột thừa c...

### TC21 [D] ✅

- **Câu hỏi:** Bệnh nhân có tổn thương da đổi màu sắc, nốt ruồi tăng kích thước nhanh, ngứa rát vùng tổn thương và bề mặt sần sùi. Bệnh gì?
- **Expected:** D86.3
- **KG Result:** D86.3 (confidence: 100.0%)
- **AI Time:** 2.7s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn mô tả và phân tích của hệ thống đồ thị tri thức, bệnh sarcoid da (mã ICD-10: D86.3) là khả năng cao nhất. Chúng ta cần thăm khám và làm thêm các xét nghiệm để xác định chính xác....

### TC22 [I] ❌

- **Câu hỏi:** Người bệnh bị mệt mỏi, hồi hộp đánh trống ngực, khó thở nhẹ khi gắng sức. Bệnh gì?
- **Expected:** I50
- **KG Result:** I23.6 (confidence: 100.0%)
- **AI Time:** 4.5s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn đang gặp phải như mệt mỏi, hồi hộp đánh trống ngực và khó thở nhẹ khi gắng sức, kết quả phân tích đồ thị tri thức cho thấy khả năng cao nhất bạn đang bị **biến chứng huyết khối trong buồng tim tâm nhĩ, tiểu nhĩ và tâm thất sau nhồi máu cơ tim cấp (ICD-10: I23.6...

### TC23 [K] ✅

- **Câu hỏi:** Tôi ăn xong thường bị ợ nóng, đau rát sau xương ức, và có cảm giác trào ngược. Bệnh gì?
- **Expected:** K29.1
- **KG Result:** K29.1 (confidence: 100.0%)
- **AI Time:** 3.9s
- **AI Answer:** Chào bạn, những triệu chứng bạn mô tả như ợ nóng, đau rát sau xương ức và cảm giác trào ngược rất phù hợp với tình trạng viêm dạ dày cấp (ICD-10: K29.1). Các triệu chứng này bao gồm đau thượng vị, khó tiêu, và buồn nôn, đều khớp với bệnh lý này. Chúng tôi sẽ cần thăm khám kỹ hơn để xác định chính xá...

### TC24 [D] ✅

- **Câu hỏi:** Bệnh nhân da xanh xao, vàng da vàng mắt, nước tiểu sẫm màu và lách to. Có phải suy tủy xương?
- **Expected:** D56.0
- **KG Result:** D56.0 (confidence: 100.0%)
- **AI Time:** 4.9s
- **AI Answer:** Chào bạn, với các triệu chứng bạn đang gặp phải như da xanh xao, vàng da vàng mắt, nước tiểu sẫm màu và lách to, kết quả phân tích đồ thị tri thức y khoa cho thấy khả năng cao nhất là Alpha thalassaemia (D56.0). 

Mặc dù các triệu chứng này có thể liên quan đến suy tủy xương, nhưng dựa trên dữ liệu ...

### TC25 [X] ❌

- **Câu hỏi:** Sau khi hít phải khí lạ, bệnh nhân buồn nôn, nôn mửa, chóng mặt, đau bụng và co giật. Chẩn đoán gì?
- **Expected:** X47
- **KG Result:** X48 (confidence: 100.0%)
- **AI Time:** 2.9s
- **AI Answer:** Chào bạn, dựa trên những triệu chứng bạn mô tả và phân tích từ đồ thị tri thức, khả năng cao nhất là bạn đã bị ngộ độc do phơi nhiễm chất diệt cỏ độc hại (ICD-10: X48).  Cần nhập viện ngay để được điều trị và làm rõ nguyên nhân....

