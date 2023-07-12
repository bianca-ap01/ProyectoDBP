<template>
  <div>
    <SolveQuiz
      :title="title"
      :max_score="max_score"
      :questions="questions"
      :quizCompleted="quizCompleted"
      :currentQuestion="currentQuestion"
    />
  </div>
</template>

<script>
import SolveQuiz from "@/components/SolveQuiz";
import { getQuizByName } from "@/services/quizzes.api";

export default {
  name: "QuizView",
  components: {
    SolveQuiz,
  },
  mounted() {
    this.getQuiz();
  },
  data() {
    return {
      title: "",
      max_score: 0,
      questions: [],
      quizCompleted: false,
      currentQuestion: 0,
    };
  },
  methods: {
    async getQuiz() {
      const { success, t, questions, mx } = await getQuizByName(
        this.$route.params.name
      );
      if (success) {
        this.title = t;
        this.max_score = mx;
        this.questions = questions;
      } else {
        this.$router.push("/dashboard");
      }
    },
    setAnswer(answer) {
      this.questions[this.currentQuestion].selected = answer;
    },
    nextQuestion() {
      if (this.currentQuestion < this.questions.length - 1) {
        this.currentQuestion++;
      } else {
        this.quizCompleted = true;
      }
    },
    getCurrentQuestion() {
      return this.questions[this.currentQuestion];
    },
    score() {
      return this.questions.filter((q) => q.answer == q.selected).length;
    },
  },
};
</script>

<style></style>
