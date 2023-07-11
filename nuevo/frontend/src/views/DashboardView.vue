<template>
  <div>
    <div v-for="quiz in quizzes" :key="quiz.id">
      <div>{{ quiz.title }}</div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { getAllQuizzes } from "@/services/quizzes.api";

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
      const { success, quizzes } = await getAllQuizzes();
      if (success) {
        this.allQuizzes = quizzes;
      }
    },
  },
};
</script>
