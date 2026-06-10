# 📊 Báo Cáo Đánh Giá Hệ Thống GraphRAG

**Ngày đánh giá:** 10/06/2026 10:01
**Model AI:** gemma3
**Số test cases:** 25

---

## 1. Kết Quả Đánh Giá Thủ Công

| Metric | Giá trị |
|--------|--------|
| KG Accuracy | 16/25 (64.0%) |
| AI Response Rate | 100.0% |
| Avg KG Confidence | 99.0% |
| Avg Response Time | 4.3s |

### Phân Tích Theo Nhóm Bệnh

| Nhóm | Đúng/Tổng | Accuracy |
|------|-----------|----------|
| D | 4/7 | 57% |
| I | 3/5 | 60% |
| J | 3/4 | 75% |
| K | 5/6 | 83% |
| X | 1/3 | 33% |

## 2. Kết Quả RAGAS

| Metric | Score |
|--------|-------|
| Raw Results | {'faithfulness': 0.5243, 'answer_relevancy': nan, 'llm_context_precision_without_reference': 0.9565, 'context_recall': 0.8636} |

## 3. Chi Tiết Từng Test Case

### TC01 [J] ✅

- **Câu hỏi:** Tôi bị sốt cao đột ngột, đau mỏi cơ khớp, đau đầu, hắt hơi sổ mũi và ho khan. Tôi có thể bị bệnh gì?
- **Expected:** J09
- **KG Result:** J09 (confidence: 95.0%)
- **AI Time:** 4.8s
- **AI Answer:** Chào bạn, với các triệu chứng bạn mô tả như sốt cao đột ngột, đau mỏi cơ khớp, đau đầu, ho khan và hắt hơi sổ mũi, đồ thị tri thức y khoa cho thấy khả năng cao nhất bạn bị Cúm do virus (ICD-10: J09) với độ tin cậy rất cao. Tuy nhiên, vẫn cần loại trừ các khả năng khác như Cúm kèm viêm phổi hoặc Cúm ...

### TC02 [J] ✅

- **Câu hỏi:** Bệnh nhân ho kèm đờm đục, sốt cao run rẩy, đau ngực khi hít thở sâu và khó thở. Chẩn đoán có thể là gì?
- **Expected:** J18.0
- **KG Result:** J18.0 (confidence: 95.0%)
- **AI Time:** 5.4s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn mô tả (ho kèm đờm đục, sốt cao run rẩy, đau ngực khi hít thở sâu, khó thở), khả năng cao nhất là **Viêm phế quản phổi (ICD-10: J18.0) với độ tin cậy 95.00%**.

Tuy nhiên, chúng tôi cũng cần loại trừ các khả năng khác như Viêm phổi do *E. coli, Klebsiella pneumo...

### TC03 [J] ✅

- **Câu hỏi:** Tôi bị khó thở tiến triển, ho khan kéo dài, giảm khả năng gắng sức và đau tức ngực. Bệnh này là gì?
- **Expected:** J61
- **KG Result:** J61 (confidence: 100.0%)
- **AI Time:** 4.7s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn mô tả và phân tích của hệ thống, khả năng cao nhất là bạn đang bị **Bệnh bụi phổi amian và các sợi khóang (J61)**. Các triệu chứng này cũng có thể liên quan đến Biểu hiện cấp tính hoặc mãn tính ở phổi do phóng xạ (J70.0) hoặc Bệnh Flax - Dresser (J66.1), tuy nh...

### TC04 [I] ✅

- **Câu hỏi:** Bệnh nhân đau đầu dữ dội đột ngột, nôn vọt, cứng gáy và rối loạn ý thức. Đây có phải xuất huyết não không?
- **Expected:** I60
- **KG Result:** I60 (confidence: 100.0%)
- **AI Time:** 4.7s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn mô tả như đau đầu dữ dội đột ngột, nôn vọt, cứng gáy và rối loạn ý thức, kết quả phân tích đồ thị tri thức cho thấy khả năng cao nhất là xuất huyết dưới màng nhện. Các triệu chứng này hoàn toàn phù hợp với chẩn đoán xuất huyết não, bao gồm cả các loại xuất huyế...

### TC05 [I] ✅

- **Câu hỏi:** Bệnh nhân bị liệt nửa người, méo miệng, nói khó và rối loạn ý thức đột ngột. Chẩn đoán gì?
- **Expected:** I64
- **KG Result:** I64 (confidence: 95.0%)
- **AI Time:** 3.8s
- **AI Answer:** Dựa trên thông tin hiện có, khả năng cao nhất là đột quỵ do xuất huyết hoặc nhồi máu não (Tai biến mạch máu não - ICD-10: I64) với độ tin cậy 95.00%. Các triệu chứng liệt nửa người và méo miệng phù hợp với chẩn đoán này. Cần phải thăm khám và làm thêm các xét nghiệm để xác định chính xác và loại trừ...

### TC06 [I] ✅

- **Câu hỏi:** Tôi bị nhức đầu vùng chẩm, hoa mắt chóng mặt, mặt đỏ bừng và ù tai. Có phải tăng huyết áp không?
- **Expected:** I10
- **KG Result:** I10 (confidence: 100.0%)
- **AI Time:** 4.7s
- **AI Answer:** Chào bạn, các triệu chứng bạn đang gặp phải (nhức đầu vùng chẩm, hoa mắt chóng mặt, mặt đỏ bừng, ù tai) rất phù hợp với bệnh tăng huyết áp. Theo phân tích dữ liệu, khả năng cao nhất bạn đang bị tăng huyết áp (ICD-10: I10) với độ tin cậy 100%. Tuy nhiên, cần thăm khám thêm để loại trừ các bệnh lý liê...

### TC07 [K] ✅

- **Câu hỏi:** Bệnh nhân đau hố chậu phải dữ dội, sốt nhẹ và buồn nôn. Có phải viêm ruột thừa không?
- **Expected:** K35
- **KG Result:** K35 (confidence: 100.0%)
- **AI Time:** 3.6s
- **AI Answer:** Chào bạn, triệu chứng đau hố chậu phải dữ dội kèm sốt nhẹ và buồn nôn của bạn rất phù hợp với tình trạng viêm ruột thừa cấp. Dựa trên phân tích hiện tại, bệnh viêm ruột thừa cấp (mã ICD-10 K35) là khả năng cao nhất, với độ tin cậy 100%. Chúng ta sẽ cần làm thêm các xét nghiệm để xác nhận chẩn đoán n...

### TC08 [K] ✅

- **Câu hỏi:** Tôi bị đau hạ sườn phải, vàng da và buồn nôn. Bệnh gì vậy?
- **Expected:** K82.0
- **KG Result:** K82.0 (confidence: 100.0%)
- **AI Time:** 3.9s
- **AI Answer:** Chào bạn, với các triệu chứng đau hạ sườn phải, vàng da và buồn nôn của bạn, hệ thống phân tích cho thấy khả năng cao nhất là tắc túi mật. Tuy nhiên, cũng cần xem xét các khả năng như sỏi mật hoặc sỏi túi mật không viêm đường mật, vì chúng cũng có các triệu chứng tương tự. Để xác định chính xác bệnh...

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
- **AI Time:** 3.9s
- **AI Answer:** Chào bạn, với các triệu chứng bạn đang gặp phải như tiêu phân có máu, đau bụng và tiêu chảy kéo dài, hệ thống phân tích cho thấy bạn có khả năng cao bị **Viêm loét đại tràng chảy máu** (ICD-10: K51). Đây là tình trạng đáng lo ngại, cần được thăm khám và điều trị kịp thời. Chúng ta sẽ cần làm thêm cá...

### TC11 [K] ✅

- **Câu hỏi:** Bệnh nhân đau hạ sườn phải, sốt cao và buồn nôn. Có phải viêm túi mật?
- **Expected:** K80.0
- **KG Result:** K80.0 (confidence: 100.0%)
- **AI Time:** 4.9s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng đau hạ sườn phải, sốt cao và buồn nôn của bạn, kết quả phân tích đồ thị tri thức y khoa cho thấy khả năng cao nhất là bạn bị sỏi túi mật có viêm túi mật cấp (mã bệnh ICD-10: K80.0). Các triệu chứng này rất giống với viêm túi mật cấp và nhồi máu gan, nhưng với độ ti...

### TC12 [D] ✅

- **Câu hỏi:** Tôi bị da xanh xao, mệt mỏi hoa mắt chóng mặt, móng tay khô dễ gãy và nhịp tim nhanh khi gắng sức. Thiếu máu phải không?
- **Expected:** D50.1
- **KG Result:** D50.1 (confidence: 100.0%)
- **AI Time:** 4.6s
- **AI Answer:** Chào bạn, các triệu chứng bạn mô tả như da xanh xao, mệt mỏi hoa mắt chóng mặt, móng tay khô dễ gãy và nhịp tim nhanh khi gắng sức gợi ý khả năng thiếu máu rất cao. Dựa trên phân tích đồ thị tri thức, việc thiếu sắt do khó nuốt là khả năng có độ tin cậy 100%. Chúng ta cần làm thêm các xét nghiệm để ...

### TC13 [D] ❌

- **Câu hỏi:** Bệnh nhân da xanh xao, vàng da vàng mắt, nước tiểu sẫm màu và lách to. Đây là bệnh gì?
- **Expected:** D56
- **KG Result:** D56.0 (confidence: 100.0%)
- **AI Time:** 3.6s
- **AI Answer:** Chào bạn, với các triệu chứng bạn mô tả như da xanh xao, vàng da vàng mắt, nước tiểu sẫm màu và lách to, kết quả phân tích đồ thị tri thức y khoa cho thấy khả năng cao nhất là **bệnh Thalassemia (Alpha thalassaemia – ICD-10: D56.0)**. Các triệu chứng này rất điển hình cho bệnh lý này.
...

### TC14 [D] ✅

- **Câu hỏi:** Tôi bị chấm nốt xuất huyết dưới da, chảy máu chân răng mũi, xuất huyết tiêu hóa và thời gian chảy máu kéo dài. Bệnh gì?
- **Expected:** D69
- **KG Result:** D69 (confidence: 100.0%)
- **AI Time:** 5.2s
- **AI Answer:** Chào bạn, với các triệu chứng bạn mô tả như chấm nốt xuất huyết dưới da, chảy máu chân răng mũi, xuất huyết tiêu hóa và thời gian chảy máu kéo dài, hệ thống phân tích cho thấy khả năng cao nhất là bạn đang bị Ban xuất huyết và các tình trạng xuất huyết khác (D69) với độ tin cậy 100%. Các triệu chứng...

### TC15 [D] ❌

- **Câu hỏi:** Bệnh nhân bị nhiễm trùng tái phát liên tục, sốt cao dai dẳng, loét niêm mạc miệng và hạch ngoại vi sưng to. Chẩn đoán gì?
- **Expected:** D84
- **KG Result:** D86 (confidence: 100.0%)
- **AI Time:** 2.6s
- **AI Answer:** Dựa trên các triệu chứng của bệnh nhân, chẩn đoán có khả năng cao nhất là **Bệnh sarcoid (Mã bệnh ICD-10: D86)**. Đồ thị tri thức y khoa cho thấy khả năng này đạt 100%....

### TC16 [D] ✅

- **Câu hỏi:** Bệnh nhân nữ bị ra khí hư bất bất thường, chảy máu âm đạo bất thường, đau vùng hạ vị và kinh nguyệt không đều. Có phải ung thư cổ tử cung?
- **Expected:** D06
- **KG Result:** D06 (confidence: 100.0%)
- **AI Time:** 4.6s
- **AI Answer:** Chào bạn, với các triệu chứng bạn đang gặp phải như ra khí hư bất thường, chảy máu âm đạo bất thường, đau vùng hạ vị và kinh nguyệt không đều, hệ thống phân tích đồ thị tri thức y khoa cho thấy khả năng cao nhất là ung thư cổ tử cung (ICD-10: D06) với độ tin cậy 100%. Tuy nhiên, cần phải thăm khám v...

### TC17 [X] ❌

- **Câu hỏi:** Bệnh nhân bị buồn nôn, nôn mửa, chóng mặt, đau bụng và co giật sau khi bị nhện cắn. Bệnh gì?
- **Expected:** X21
- **KG Result:** X41 (confidence: 100.0%)
- **AI Time:** 5.0s
- **AI Answer:** Chào bạn,

Dựa trên các triệu chứng bạn mô tả (buồn nôn, nôn mửa, chóng mặt, đau bụng, co giật) và tiền sử bạn kể là bị nhện cắn, khả năng cao nhất là bạn đã bị ngộ độc do phơi nhiễm thuốc chống động kinh, an thần – gây ngủ, chống parkinson, tâm thần.  Việc nhện cắn có thể là một yếu tố kích thích, ...

### TC18 [X] ✅

- **Câu hỏi:** Bệnh nhân buồn nôn, nôn mửa, chóng mặt, đau bụng và co giật sau khi uống rượu quá nhiều. Đây là gì?
- **Expected:** X45
- **KG Result:** X45 (confidence: 100.0%)
- **AI Time:** 5.1s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn mô tả (buồn nôn, nôn mửa, chóng mặt, đau bụng, co giật) và tiền sử uống rượu quá nhiều, khả năng cao nhất là bạn đang bị **tai nạn ngộ độc và phơi nhiễm rượu** (ICD-10: X45). Triệu chứng co giật, chóng mặt, buồn nôn, đau bụng, nôn mửa đều phù hợp với tình trạng...

### TC19 [I] ❌

- **Câu hỏi:** Bệnh nhân đau di chuyển các khớp lớn, có tiếng thổi ở tim, hồi hộp đánh trống ngực và khó thở nhẹ khi gắng sức. Bệnh gì?
- **Expected:** I08.9
- **KG Result:** I23.6 (confidence: 95.0%)
- **AI Time:** 3.9s
- **AI Answer:** Chào bệnh nhân, dựa trên các triệu chứng của bác, kết quả phân tích đồ thị tri thức y khoa cho thấy khả năng cao nhất là bệnh nhân đang bị **biến chứng huyết khối trong buồng tim, tiểu nhĩ và tâm thất sau nhồi máu cơ tim cấp (I23.6)**. Bác cần được thăm khám và làm thêm các xét nghiệm để xác định ch...

### TC20 [J] ❌

- **Câu hỏi:** Trẻ em bị sốt nhẹ, chảy mũi, đau họng và ho. Có phải viêm đường hô hấp trên?
- **Expected:** J06.9
- **KG Result:** K35 (confidence: 95.0%)
- **AI Time:** 5.1s
- **AI Answer:** Chào bạn,

Dựa trên các triệu chứng bạn đang gặp phải (sốt nhẹ, chảy mũi, đau họng, ho), hệ thống phân tích hiện tại cho thấy viêm ruột thừa cấp có khả năng cao nhất (95.00%) và phù hợp với các triệu chứng sốt nhẹ. Mặc dù các triệu chứng của bạn có thể liên quan đến viêm đường hô hấp trên, nhưng cần...

### TC21 [D] ❌

- **Câu hỏi:** Bệnh nhân có tổn thương da đổi màu sắc, nốt ruồi tăng kích thước nhanh, ngứa rát vùng tổn thương và bề mặt sần sùi. Bệnh gì?
- **Expected:** D04
- **KG Result:** D86.3 (confidence: 100.0%)
- **AI Time:** 2.3s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn mô tả và phân tích của hệ thống, bệnh có khả năng cao nhất là **bệnh sarcoid da** (ICD-10: D86.3)....

### TC22 [I] ❌

- **Câu hỏi:** Người bệnh bị mệt mỏi, hồi hộp đánh trống ngực, khó thở nhẹ khi gắng sức. Bệnh gì?
- **Expected:** I50
- **KG Result:** I23.6 (confidence: 100.0%)
- **AI Time:** 5.0s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn trình bày (mệt mỏi, hồi hộp đánh trống ngực, khó thở nhẹ khi gắng sức), kết quả phân tích đồ thị tri thức y khoa cho thấy bệnh có khả năng cao nhất là **biến chứng huyết khối trong buồng tim tâm nhĩ, tiểu nhĩ và tâm thất sau nhồi máu cơ tim cấp (Mã bệnh ICD-10:...

### TC23 [K] ❌

- **Câu hỏi:** Tôi ăn xong thường bị ợ nóng, đau rát sau xương ức, và có cảm giác trào ngược. Bệnh gì?
- **Expected:** K21
- **KG Result:** K29.1 (confidence: 100.0%)
- **AI Time:** 4.0s
- **AI Answer:** Chào bạn, các triệu chứng bạn mô tả như ợ nóng, đau rát sau xương ức, và cảm giác trào ngược rất phù hợp với tình trạng viêm dạ dày cấp. Dựa trên thông tin hiện tại, khả năng cao nhất là bạn bị viêm dạ dày cấp (ICD-10: K29.1). Để xác định chính xác và có hướng điều trị tốt nhất, bạn nên đi khám bác ...

### TC24 [D] ✅

- **Câu hỏi:** Bệnh nhân da xanh xao, vàng da vàng mắt, nước tiểu sẫm màu và lách to. Có phải suy tủy xương?
- **Expected:** D56.0
- **KG Result:** D56.0 (confidence: 100.0%)
- **AI Time:** 6.5s
- **AI Answer:** Chào bạn, dựa trên những triệu chứng bạn mô tả (da xanh xao, vàng da vàng mắt, nước tiểu sẫm màu, lách to) và phân tích đồ thị tri thức, khả năng cao nhất là bạn bị Thalassemia (mã ICD-10 D56.0, D56.1 hoặc D56). Các triệu chứng này rất điển hình của bệnh Thalassemia, bao gồm lách to, da xanh xao niê...

### TC25 [X] ❌

- **Câu hỏi:** Sau khi hít phải khí lạ, bệnh nhân buồn nôn, nôn mửa, chóng mặt, đau bụng và co giật. Chẩn đoán gì?
- **Expected:** X47
- **KG Result:** X48 (confidence: 100.0%)
- **AI Time:** 3.4s
- **AI Answer:** Chào bạn, dựa trên các triệu chứng bạn mô tả và phân tích của hệ thống đồ thị tri thức, khả năng cao nhất là bạn đã bị ngộ độc do phơi nhiễm chất diệt cỏ độc hại (ICD-10: X48). Chúng tôi sẽ tiến hành thăm khám và xét nghiệm để xác định chính xác nguyên nhân và đưa ra phương án điều trị phù hợp nhất....

