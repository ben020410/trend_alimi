document.getElementById("start-button").addEventListener("click", () => {
    const startButton = document.getElementById("start-button");
    const resultsDiv = document.getElementById("results");
    const trendImage = document.querySelector(".trend-image");

    // "트렌드를 분석 중입니다..." 메시지 표시
    resultsDiv.innerHTML = "<p>트렌드를 분석 중입니다...</p>";

    // 이미지 애니메이션 시작
    let currentScene = 1;
    const totalScenes = 8;

    const imageInterval = setInterval(() => {
        currentScene = (currentScene % totalScenes) + 1;
        trendImage.src = `/static/cat_animation/scene${currentScene}.png`;
    }, 500);

    // 백엔드 요청
    fetch("/run-script", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            clearInterval(imageInterval);
            trendImage.remove();
            resultsDiv.innerHTML = "";

            if (data.length > 0) {
                const totalMessage = document.createElement("p");
                totalMessage.innerHTML = `<strong>총 ${data.length}건의 유행 아이템이 탐지되었습니다.</strong>`;
                resultsDiv.appendChild(totalMessage);

                data.forEach(item => {
                    const itemDiv = document.createElement("div");
                    itemDiv.classList.add("result-item");
                    itemDiv.innerHTML = `
                        <div class="item-name">${item.title}</div>
                        <div class="item-details">
                            <p><strong>유행 점수:</strong> ${item.max_tv_score}</p>
                            <p><strong>유행 시기:</strong> ${item.period}</p>
                        </div>
                    `;
                    resultsDiv.appendChild(itemDiv);
                });

                startButton.style.display = "none";
            } else {
                resultsDiv.innerHTML = "<p>2주 이내 유행 아이템이 없습니다.</p>";
                startButton.style.display = "none";
            }
        })
        .catch(err => {
            clearInterval(imageInterval);
            console.error("Error fetching data:", err);
            alert("오류가 발생했습니다. 다시 시도해주세요.");
        });
});
