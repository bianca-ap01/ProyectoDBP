<template>
  <main class="app">
    <h1>{{ title }}</h1>

    <section class="quiz" v-if="!quizCompleted">
      <div class="quiz-info">
        <span class="question">{{ getCurrentQuestion.question }}</span>
        <span class="score">Score {{ score }}/{{ max_score }}</span>
      </div>

      <div class="options">
        <label
          v-for="(option, index) in getCurrentQuestion.options"
          :key="index"
          :for="'option' + index"
          :class="`option ${
            getCurrentQuestion.selected == index
              ? index == getCurrentQuestion.answer
                ? 'correct'
                : 'wrong'
              : ''
          } ${
            getCurrentQuestion.selected != null &&
            index != getCurrentQuestion.selected
              ? 'disabled'
              : ''
          }`"
        >
          <input
            type="radio"
            :id="'option' + index"
            :name="getCurrentQuestion.index"
            :value="index"
            v-model="getCurrentQuestion.selected"
            :disabled="getCurrentQuestion.selected"
            @change="setAnswer"
          />
          <span>{{ option }}</span>
        </label>
      </div>

      <button @click="nextQuestion" :disabled="!getCurrentQuestion.selected">
        {{
          getCurrentQuestion.index === questions.length - 1
            ? "Finish"
            : getCurrentQuestion.selected === null
            ? "Select an option"
            : "Next question"
        }}
      </button>
    </section>

    <section v-else>
      <h2>You have finished the quiz!</h2>
      <p>Your score is {{ score }}/{{ questions.length }}</p>
    </section>
  </main>
</template>

<script>
import { getQuizByName } from "@/services/quizzes.api";

export default {
  name: "QuizComponent",
  data() {
    return {
      quiz: getQuizByName(this.$route.params.name),
      title: null,
      max_score: null,
      questions: [],
      quizCompleted: false,
      currentQuestion: 0,
    };
  },
  computed: {
    score() {
      let value = 0;
      this.questions.forEach((q) => {
        if (q.selected !== null && q.answer === q.selected) {
          console.log("correct");
          value++;
        }
      });
      return value;
    },
    getCurrentQuestion() {
      let question = this.questions[this.currentQuestion];
      question.index = this.currentQuestion;
      return question;
    },
  },
  methods: {
    setAnswer(e) {
      this.questions[this.currentQuestion].selected = e.target.value;
      e.target.value = null;
    },
    nextQuestion() {
      if (this.currentQuestion < this.questions.length - 1) {
        this.currentQuestion++;
      } else {
        this.quizCompleted = true;
      }
    },
  },
  created() {
    this.title = this.quiz.title;
    this.max_score = this.quiz.max_score;

    for (let i = 0; i < this.quiz.questions.length; i++) {
      let temp = {};
      temp.question = this.quiz.questions[i].question;
      temp.answer = this.quiz.questions[i].answer;

      let options = [];
      for (let j = 0; j < this.quiz.questions[i].options.length; j++) {
        options.push(this.quiz.questions[i].options[j].option);
      }
      temp.options = options;

      temp.selected = null;

      this.questions.push(temp);
    }
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Montserrat", sans-serif;
}

body {
  background-color: #271c36;
  color: #fff;
}

.app {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  height: 100vh;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
}

.quiz {
  background-color: #382a4b;
  padding: 1rem;
  width: 100%;
  max-width: 640px;
}

.quiz-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.quiz-info .question {
  color: #8f8f8f;
  font-size: 1.25rem;
}

.quiz-info.score {
  color: #fff;
  font-size: 1.25rem;
}

.options {
  margin-bottom: 1rem;
}

.option {
  padding: 1rem;
  display: block;
  background-color: #271c36;
  margin-bottom: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
}

.option:hover {
  background-color: #2d213f;
}

.option.correct {
  background-color: #2cce7d;
}

.option.wrong {
  background-color: #ff5a5f;
}

.option:last-of-type {
  margin-bottom: 0;
}

.option.disabled {
  opacity: 0.5;
}

.option input {
  display: none;
}

button {
  appearance: none;
  outline: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem 1rem;
  background-color: #2cce7d;
  color: #2d213f;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 1.2rem;
  border-radius: 0.5rem;
}

button:disabled {
  opacity: 0.5;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
}

p {
  color: #8f8f8f;
  font-size: 1.5rem;
  text-align: center;
}
</style>
