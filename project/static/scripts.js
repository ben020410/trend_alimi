document.getElementById("start-button").addEventListener("click", () => {
    const startButton = document.getElementById("start-button");
    const resultsDiv = document.getElementById("results");

    // "트렌드를 분석 중입니다..." 메시지 표시
    resultsDiv.innerHTML = "<p>트렌드를 분석 중입니다...</p>";

    fetch("/run-script", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            // 결과 초기화
            resultsDiv.innerHTML = "";

            if (data.length > 0) {
                // "총 N건의 유행 아이템이 탐지되었습니다." 메시지
                const totalMessage = document.createElement("p");
                totalMessage.innerHTML = `<strong>총 ${data.length}건의 유행 아이템이 탐지되었습니다.</strong>`;
                resultsDiv.appendChild(totalMessage);

                // 각 유행 아이템의 세부 정보 표시
                data.forEach(item => {
                    const itemDiv = document.createElement("div");
                    itemDiv.classList.add("result-item");
                    itemDiv.innerHTML = `
                        <p><strong>아이템 이름:</strong> ${item.title}</p>
                        <p><strong>TV Score:</strong> ${item.max_tv_score}</p>
                        <p><strong>Period:</strong> ${item.period}</p>
                    `;
                    resultsDiv.appendChild(itemDiv);
                });

                // "시작" 버튼 숨기기
                startButton.style.display = "none";
            } else {
                // 결과가 없을 때
                resultsDiv.innerHTML = "<p>2주 이내 유행 아이템이 없습니다.</p>";
                startButton.style.display = "none"; // 버튼 숨기기
            }
        })
        .catch(err => {
            console.error("Error fetching data:", err);
            alert("오류가 발생했습니다. 다시 시도해주세요.");
        });
});
