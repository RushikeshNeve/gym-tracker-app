export type TimetableOptionGroup = {
  category: string;
  options: string[];
  setsReps: string;
};

export type TimetableDay = {
  id: string;
  dayLabel: string;
  title: string;
  subtitle: string;
  accent: "primary" | "secondary" | "warning";
  notes?: string[];
  images: string[];
  blocks: TimetableOptionGroup[];
};

export const weeklySplit = [
  { day: "Day 1", workout: "Push" },
  { day: "Day 2", workout: "Pull" },
  { day: "Day 3", workout: "Legs" },
  { day: "Day 4", workout: "Push" },
  { day: "Day 5", workout: "Pull" },
  { day: "Day 6", workout: "Cardio + Core" },
  { day: "Day 7", workout: "Rest" },
];

export const timetableDays: TimetableDay[] = [
  {
    id: "push",
    dayLabel: "Day 1 & 4",
    title: "Push",
    subtitle: "Chest + Shoulders + Triceps",
    accent: "primary",
    images: [
      "https://www.puregym.com/media/h3gjo30x/dumbbell-bench-press.jpg?quality=80",
      "https://blog.myarsenalstrength.com/hubfs/chest%20press.webp",
      "https://cdn.muscleandstrength.com/sites/default/files/standing-high-to-low-cable-fly-1.jpg",
      "https://www.chrisadamspersonaltraining.com/uploads/1/3/2/1/132150751/published/screenshot-20210803-132234-gallery.jpg?1628000356=",
      "https://cdn.shopify.com/s/files/1/0618/9462/3460/files/stock-photo-beautiful-young-caucasian-female-athlete-exercising-with-cable-crossover-machine-in-fitness-gym-1846648126-800x571.jpg",
    ],
    blocks: [
      { category: "Chest Press", options: ["Dumbbell Press", "Smith Machine Press", "Barbell Bench Press"], setsReps: "3 x 8-12" },
      { category: "Incline Chest", options: ["Incline Machine Press", "Incline DB Press", "Incline Smith Press"], setsReps: "3 x 8-12" },
      { category: "Chest Isolation", options: ["Cable Crossover", "Pec Deck", "Chest Fly (DB)"], setsReps: "3 x 10-12" },
      { category: "Shoulders", options: ["Cable Lateral Raise", "DB Lateral Raise", "Machine Lateral Raise"], setsReps: "3 x 12-15" },
      { category: "Triceps 1", options: ["Cable Pushdown", "Skull Crusher", "Dips"], setsReps: "3 x 10-12" },
      { category: "Triceps 2", options: ["Overhead Cable Ext", "DB Overhead Ext", "Rope Extension"], setsReps: "3 x 10-12" },
    ],
  },
  {
    id: "pull",
    dayLabel: "Day 2 & 5",
    title: "Pull",
    subtitle: "Back + Biceps",
    accent: "secondary",
    images: [
      "https://www.puregym.com/media/mmijlfwq/wide-grip-lat-pulldown.jpg?quality=80",
      "https://www.puregym.com/media/0epkvais/seated-row.jpg?quality=80",
      "https://www.soletreadmills.com/cdn/shop/articles/A_man_doing_a_barbell_bent_over_row..png?v=1751312161&width=2048",
      "https://blog.myarsenalstrength.com/hs-fs/hubfs/Bent%20over%20row%20exercise.png",
      "https://hips.hearstapps.com/menshealth-uk/main/assets/row-under.gif",
    ],
    blocks: [
      { category: "Vertical Pull", options: ["Lat Pulldown", "Assisted Pull-ups", "Pull-ups"], setsReps: "3 x 8-12" },
      { category: "Row (Wide)", options: ["Machine Row Wide", "Cable Row Wide", "Barbell Row"], setsReps: "3 x 8-12" },
      { category: "Row (Close)", options: ["Close Grip Row", "Seated Cable Row", "T-Bar Row"], setsReps: "3 x 8-12" },
      { category: "Traps", options: ["DB Shrugs", "Barbell Shrugs", "Machine Shrugs"], setsReps: "3 x 10-12" },
      { category: "Biceps 1", options: ["Machine Curl", "Barbell Curl", "EZ Curl"], setsReps: "3 x 10-12" },
      { category: "Biceps 2", options: ["Hammer Curl", "Rope Curl", "Incline DB Curl"], setsReps: "3 x 10-12" },
    ],
  },
  {
    id: "legs",
    dayLabel: "Day 3",
    title: "Legs",
    subtitle: "Strength Focus",
    accent: "warning",
    images: [
      "https://bellsofsteel.com/cdn/shop/articles/How-To-Use-Hack-Squat-Machine.webp?v=1708539914&width=1024",
      "https://hips.hearstapps.com/hmg-prod/images/woman-lifting-weight-on-legs-royalty-free-image-1704915259.jpg?crop=0.670xw%3A1.00xh%3B0.0801xw%2C0&resize=1200%3A%2A",
      "https://www.puregym.com/media/5gwmhhys/romanian-deadlift.jpg?quality=80",
      "https://cdn.muscleandstrength.com/sites/default/files/romanian-deadlift.jpg",
      "https://content.artofmanliness.com/uploads/2024/11/Romanian-Deadlift-1.jpg",
    ],
    blocks: [
      { category: "Squat", options: ["Hack Squat", "Smith Squat", "Barbell Squat"], setsReps: "3 x 8-12" },
      { category: "Quad Focus", options: ["Leg Press", "Bulgarian Split Squat", "Lunges"], setsReps: "3 x 10" },
      { category: "Hamstrings", options: ["Romanian Deadlift", "Stiff Leg Deadlift", "Good Mornings"], setsReps: "3 x 8-12" },
      { category: "Isolation", options: ["Leg Extension", "Sissy Squat", "Machine Quad Ext"], setsReps: "3 x 10-12" },
      { category: "Curl", options: ["Leg Curl", "Seated Curl", "Nordic Curl"], setsReps: "3 x 10-12" },
      { category: "Calves", options: ["Standing Raise", "Seated Raise", "Leg Press Calf"], setsReps: "4 x 12-15" },
    ],
    notes: ["Keep same structure on repeat days.", "Rotate exercise options after 2-3 weeks or when equipment availability changes."],
  },
  {
    id: "cardio-core",
    dayLabel: "Day 6",
    title: "Cardio + Core",
    subtitle: "Conditioning + trunk work",
    accent: "secondary",
    images: [
      "https://static.nike.com/a/images/f_auto%2Ccs_srgb/w_1536%2Cc_limit/6a2dbeb8-e877-42c1-ae92-52e1ae29799f/3-treadmill-workouts-that-can-boost-your-fitness.jpg",
      "https://jsbhealthcare.co.in/cdn/shop/files/exercise-cycle-air-bike-for-home-jsb-hf175_16ab4842-55bf-484d-8bc9-8397ab1e116e.webp?v=1759901440",
      "https://www.realsimple.com/thmb/LAvXbxPdTZGe9chMDEbUmWV19ZQ%3D/1500x0/filters%3Ano_upscale%28%29%3Amax_bytes%28150000%29%3Astrip_icc%28%29/JumpRope_Infographic-100-7cbf0af757f04e108a0756f93c7d1fad.jpg",
      "https://hips.hearstapps.com/hmg-prod/images/skip-those-worries-away-royalty-free-image-1678894439.jpg?crop=0.669xw%3A1.00xh%3B0.0226xw%2C0&resize=640%3A%2A",
      "https://cdn.shopify.com/s/files/1/0316/7810/3691/files/jump_rope_routine_HIIT_exercise_f25afb37-ff2d-4512-82fb-e47935f7ac29.jpg?v=1611754826",
    ],
    blocks: [
      { category: "Cardio", options: ["Running (25 min)", "Cycling (30 min)", "Incline Walk (25 min)"], setsReps: "Pick 1" },
      { category: "HIIT", options: ["Sprint Intervals", "Jump Rope", "Stairmaster"], setsReps: "Pick 1" },
      { category: "Core", options: ["Plank", "Hanging Leg Raise", "Russian Twists"], setsReps: "3 rounds" },
    ],
    notes: ["Pick one option per block.", "Repeat the structure and gradually add time, reps, or intensity."],
  },
];
