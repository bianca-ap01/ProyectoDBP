<template>
  <div>
    <div v-for="quiz in allQuizzes" :key="quiz.id">
      <div>{{ quiz.title }}</div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { fetchSurveys } from "@/services/quizzes.api";

export default {
  name: "HomeView",
  components: {},
  mounted() {
    this.loadQuizzes();
  },
  data() {
    return {
      allQuizzes: [],
    };
  },
  methods: {
    async loadQuizzes() {
      const { success, quizzes } = await fetchSurveys();
      if (success) {
        this.allQuizzes = quizzes;
      }
    },
  },
};
</script>
