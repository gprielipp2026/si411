#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdbool.h>

//#define NTHREADS 3 

#define MAX_SIZE 1000 		// How many to read
#define FILENAME "numbers.txt"

void* check_primes(void* vargs);

void printResults();

// Global variables (accessible by all threads)
int numbers[MAX_SIZE];           // will be read from file
int primesFound[MAX_SIZE];       // will hold the primes that are found
int primesFoundCount = 0;        // how many primes found so far??

typedef struct {
  int start; //inclusive
  int stop; //exlusive
  int count;
  int tid;
} args_t;

pthread_mutex_t lock;

int main()
{
  int i;
  
  // Ensure memory is empty to start
  for (i=0; i<MAX_SIZE; i++) {
    primesFound[i] = 0;
  }
  
  // Read numbers from file, store into array
  FILE * file = fopen (FILENAME, "r");
  if (file == NULL) {
    printf("Error opening %s\n", FILENAME);
    exit(1);
  }
  i = 0;
  while ((!feof(file)) && (i < MAX_SIZE)) {  
    fscanf (file, "%d", &numbers[i]);    
    i++;
  }
  fclose (file);        

  // TODO: remove or comment out the next line for the multi-threaded version:
  //check_primes();
  
  // TODO: create the threads, and have each one execute 'check_primes'
  pthread_mutex_init(&lock, NULL);
  pthread_t threads[NTHREADS];
  float numPerThread = (float)MAX_SIZE / (float)NTHREADS;
  args_t args[NTHREADS];
  for(int i = 0; i < NTHREADS; i++)
  {
    int start = (int)(i * numPerThread), 
        stop = (int)((i+1) * numPerThread);
    
    args[i] = (args_t){.start = start, .stop = stop, .count = 0, .tid = i};
    
    pthread_create(&threads[i], NULL, check_primes, &args[i]);
  }


  // TODO: join threads when complete
  for(int i = 0; i < NTHREADS; i++)
  {
    pthread_join(threads[i], NULL);
  }
  pthread_mutex_destroy(&lock);
  // Print the results

  int sum = 0;
  for(int i = 0; i < NTHREADS; i++)
  {
    sum += args[i].count;
  }

  printf ("Found a total of %d primes.\n", sum);
  // TODO (later!): uncomment printResults() when instructed to do so
  //printResults();  
}

// Print out all the primes that were found
void printResults() {
  int i;
  for (i=0; i<primesFoundCount; i++) {
    printf("%d ", primesFound[i]);
  }
  printf ("\n");
}

// Returns true if 'num' is prime
bool isPrime(int num) {
  if (num <= 1) return false;
  for (int j = 2; j < num; j++) {
    if (num % j == 0) {
      return false;
    }
  }
  return true;  // no factor found, so must be prime
}

// Check all values in the array numbers[], and place any primes found in the primesFound[] array.
void* check_primes(void* vargs)
{
  // TODO: make any necessary changes so that each thread can call this function AND
  //   have the 'work' divided evenly among the threads.
  //   Do NOT make multiple copies of any code!
  //   Also, your code must work work any value of NTHREADS
  
  args_t* args = (args_t*)vargs;
  //printf("start = %d, stop = %d\n", args->start, args->stop);
  

  int i   = 0;
  int num = 0;

  for (i=args->start; i<args->stop; i++) {
    num = numbers[i];
    if (isPrime(num)) {
      pthread_mutex_lock(&lock);
      primesFound[primesFoundCount] = num;
      //printf("thread %d found %d \n",args->tid, num);
      primesFoundCount++;
      args->count++;
      pthread_mutex_unlock(&lock);
    }
  }
  return 0;
}
