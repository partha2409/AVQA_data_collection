const socket = io.connect();

socket.on('message', (message) => {
    console.log(message);
});

window.addEventListener('beforeunload', () => {
    socket.disconnect();
});

const all_entries = ['yes_or_no_q1', 'yes_or_no_ans1', 'yes_or_no_q2','yes_or_no_ans2', 'desc_q1', 'desc_ans1', 'desc_q2', 'desc_ans2', 'logical_q1', 'logical_ans1', 'logical_q2', 'logical_ans2', 'next-task']
const five_word_entries = ['yes_or_no_q1', 'yes_or_no_q2', 'desc_q1', 'desc_ans1', 'desc_q2', 'desc_ans2', 'logical_q1', 'logical_ans1', 'logical_q2', 'logical_ans2']



document.querySelector("video").onended = function() {
  console.log('hello')
  if(this.played.end(0) - this.played.start(0) === this.duration) {
        for (let i = 0; i < all_entries.length; i++)
        {
            document.getElementById(all_entries[i]).removeAttribute("disabled");
        }}
  else {
    window.alert('Please do not skip the video.')
  }
}

document.getElementById('task-form').addEventListener('submit', function(event) {
    for (let i = 0; i < all_entries.length; i++) {
            const textarea = document.getElementById(all_entries[i]);
            if (textarea.value.trim() === '') {
                window.alert('Please fill all the text boxes.')
                event.preventDefault();
                return
            }
        }

    for (let i = 0; i < five_word_entries.length; i++) {
            const textarea = document.getElementById(five_word_entries[i]);
            if (hasAtLeast5Words(textarea)) {
                window.alert("The description should contain at least 5 words.");
                event.preventDefault(); // Prevent form submission
                return
            }
        }

    const yes_or_no_q1 = document.getElementById('yes_or_no_q1').value;
    const yes_or_no_ans1 = document.getElementById('yes_or_no_ans1').value;
    const yes_or_no_q2 = document.getElementById('yes_or_no_q2').value;
    const yes_or_no_ans2 = document.getElementById('yes_or_no_ans2').value;

    const desc_q1 = document.getElementById('desc_q1').value;
    const desc_ans1 = document.getElementById('desc_ans1').value;
    const desc_q2 = document.getElementById('desc_q2').value;
    const desc_ans2 = document.getElementById('desc_ans2').value;

    const logical_q1 = document.getElementById('logical_q1').value;
    const logical_ans1 = document.getElementById('logical_ans1').value;
    const logical_q2 = document.getElementById('logical_q2').value;
    const logical_ans2 = document.getElementById('logical_ans2').value;

    const formData = new FormData();

    formData.append('yes_or_no_q1', yes_or_no_q1);
    formData.append('yes_or_no_ans1', yes_or_no_ans1);
    formData.append('yes_or_no_q2', yes_or_no_q2);
    formData.append('yes_or_no_ans2', yes_or_no_ans2);

    formData.append('desc_q1', desc_q1);
    formData.append('desc_ans1', desc_ans1);
    formData.append('desc_q2', desc_q2);
    formData.append('desc_ans2', desc_ans2);

    formData.append('logical_q1', logical_q1);
    formData.append('logical_ans1', logical_ans1);
    formData.append('logical_q2', logical_q2);
    formData.append('logical_ans2', logical_ans2);

    fetch('/next-task-button', {
        method: 'POST',
        body: formData
    })
});

function hasAtLeast5Words(text) {
  // Remove leading and trailing whitespaces to handle cases with extra spaces.
  const trimmedText = text.value.trim();

  // Split the string by whitespace to count the words.
  const words = trimmedText.split(/\s+/);

  // Check if the number of words is at least 5.
  return words.length < 5;
}