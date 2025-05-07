export      function initializeTimeWheels() {
        const minutesColumn = document.getElementById("minutesColumn");
        const secondsColumn = document.getElementById("secondsColumn");

        // Populate minutes (0-59)
        minutesColumn.innerHTML = '<div style="height: 100px"></div>';
        for (let i = 0; i < 60; i++) {
          const div = document.createElement("div");
          div.className = "time-item";
          div.textContent = `${i}m`;
          minutesColumn.appendChild(div);
        }
        minutesColumn.innerHTML += '<div style="height: 100px"></div>';

        // Populate seconds (0-59)
        secondsColumn.innerHTML = '<div style="height: 100px"></div>';
        for (let i = 0; i < 60; i++) {
          const div = document.createElement("div");
          div.className = "time-item";
          div.textContent = `${i}s`;
          secondsColumn.appendChild(div);
        }
        secondsColumn.innerHTML += '<div style="height: 100px"></div>';
      }
export       function setupTimeWheels() {
        const hoursColumn = document.getElementById("hoursColumn");
        const minutesColumn = document.getElementById("minutesColumn");
        const secondsColumn = document.getElementById("secondsColumn");
        const itemHeight = 40;

        const setScrollPosition = (column, value) => {
          column.scrollTop = (value * itemHeight) + 100;
        };

        setScrollPosition(hoursColumn, selectedHours);
        setScrollPosition(minutesColumn, selectedMinutes);
        setScrollPosition(secondsColumn, selectedSeconds);

        const handleScroll = (column, type) => {
          const selectedIndex = Math.round(
            (column.scrollTop - 100) / itemHeight
          );

          Array.from(column.children).forEach((item, index) => {
            if (index === selectedIndex + 1) {
              item.classList.add("selected");
              switch(type) {
                case 'hours': selectedHours = index - 1; break;
                case 'minutes': selectedMinutes = index - 1; break;
                case 'seconds': selectedSeconds = index - 1; break;
              }
            } else {
              item.classList.remove("selected");
            }
          });
        };

        hoursColumn.addEventListener("scroll", () => handleScroll(hoursColumn, 'hours'));
        minutesColumn.addEventListener("scroll", () => handleScroll(minutesColumn, 'minutes'));
        secondsColumn.addEventListener("scroll", () => handleScroll(secondsColumn, 'seconds'));
      }
export function showTimerPopup() { document.getElementById('timerPopup').style.display='block'; setupTimeWheels(); }
export function hideTimerPopup() { document.getElementById('timerPopup').style.display='none'; }
export       function setSleepTimer() {
        const totalMs = (selectedHours * 3600 + selectedMinutes * 60 + selectedSeconds) * 1000;
        if (totalMs > 0) {
          endTime = Date.now() + totalMs;

          document.querySelector(".time-selector").style.display = "none";
          document.getElementById("activeTimer").style.display = "block";

          countdownInterval = setInterval(updateCountdownDisplay, 1000);
          updateCountdownDisplay();
          showNotification("Sleep timer set");
        }
        hideTimerPopup();
      }
export       function resetSleepTimer() {
        if (countdownInterval) clearInterval(countdownInterval);
        if (sleepTimer) clearTimeout(sleepTimer);

        endTime = null;
        countdownInterval = null;
        sleepTimer = null;

        document.querySelector(".time-selector").style.display = "flex";
        document.getElementById("activeTimer").style.display = "none";
        hideTimerPopup();
        showNotification("Timer cancelled");
      }
