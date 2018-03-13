using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {
            var files = new string[] { "norm_hamlet.txt", "norm_romeo_and_juliet.txt", "norm_wiki_sample.txt" };
            var textToOpen = files[1];

            var program = new Program(textToOpen);
            program.FindApproximation();
        }
        const string Pathname = @"D:\OneDrive\pp\infa\semestrVI\t\Laboratoria\Lab1";

        string text = string.Empty;
        const string alphabet = "abcdefghijklmnopqrstuvwxyz ";
        Occurences occurences;
        Program(string textToOpen)
        {
            GetTextFromFile(textToOpen);
            //GetTextFromDebug();
            occurences = new Occurences(alphabet.Count());
        }

        private void GetTextFromDebug()
        {
            text = "aaaaa, asjdhaksaaaaaaasdasd, vaaaaaa";
        }

        public void FindApproximation()
        {
            foreach (char first in alphabet)
            {
                CreateIfNotExist(ref occurences.InnerOccurences[first.Normalize()]);
                foreach (char second in alphabet)
                {
                    CreateIfNotExist(ref occurences.InnerOccurences[first.Normalize()].InnerOccurences[second.Normalize()]);
                    CountOccurences($"{first}{second}");
                }
                CountOccurences($"{first}");
                CalculateProbabilities($"{first}");
            }
            CalculateProbabilities();


            foreach (char first in alphabet)
            {
                foreach (char second in alphabet)
                {
                    if (occurences[$"{first}"].Probabilities[second.Normalize()] > 0)
                    {
                        foreach (char third in alphabet)
                        {
                            CreateIfNotExist(ref occurences.InnerOccurences[first.Normalize()].InnerOccurences[second.Normalize()].InnerOccurences[third.Normalize()]);
                            CountOccurences($"{first}{second}{third}");
                        }
                    }
                    CalculateProbabilities($"{first}{second}");
                }
            }

            foreach (char first in alphabet)
            {
                foreach (char second in alphabet)
                {
                    foreach (char third in alphabet)
                    {
                        if (occurences[$"{first}{second}"].Probabilities[third.Normalize()] > 0)
                        {
                            foreach (char fourth in alphabet)
                            {
                                CreateIfNotExist(ref occurences.InnerOccurences[first.Normalize()].InnerOccurences[second.Normalize()].InnerOccurences[third.Normalize()].InnerOccurences[fourth.Normalize()]);
                                CountOccurences($"{first}{second}{third}{fourth}");
                            }
                        }
                        CalculateProbabilities($"{first}{second}{third}");
                    }

                }
            }

            foreach (char first in alphabet)
            {
                foreach (char second in alphabet)
                {
                    foreach (char third in alphabet)
                    {
                        if (occurences.InnerOccurences[first.Normalize()].InnerOccurences[second.Normalize()].InnerOccurences[third.Normalize()] != null)
                        {
                            foreach (char fourth in alphabet)
                            {
                                if (occurences[$"{first}{second}{third}"].Probabilities[fourth.Normalize()] > 0)
                                {
                                    foreach (char fifth in alphabet)
                                    {
                                        CreateIfNotExist(ref occurences.InnerOccurences[first.Normalize()].InnerOccurences[second.Normalize()].InnerOccurences[third.Normalize()].InnerOccurences[fourth.Normalize()].InnerOccurences[fifth.Normalize()]);
                                        CountOccurences($"{first}{second}{third}{fourth}{fifth}");
                                    }
                                }
                                CalculateProbabilities($"{first}{second}{third}{fourth}");
                            }
                        }
                    }
                }
            }
            HashSet<string> wyrazy = new HashSet<string>();
            foreach (char first in alphabet)
            {
                foreach (char second in alphabet)
                {
                    foreach (char third in alphabet)
                    {
                        if (occurences.InnerOccurences[first.Normalize()].InnerOccurences[second.Normalize()].InnerOccurences[third.Normalize()] != null)
                        {
                            foreach (char fourth in alphabet)
                            {
                                if (occurences[$"{first}{second}{third}"].Probabilities[fourth.Normalize()] > 0)
                                {
                                    foreach (char fifth in alphabet)
                                    {
                                        CreateIfNotExist(ref occurences.InnerOccurences[first.Normalize()].InnerOccurences[second.Normalize()].InnerOccurences[third.Normalize()].InnerOccurences[fourth.Normalize()].InnerOccurences[fifth.Normalize()]);
                                        CountOccurences($"{first}{second}{third}{fourth}{fifth}");
                                    }
                                }
                            }
                        }
                    }
                }
            }

        }

        const float threshold = 0f;
        private void CalculateProbabilities(string index = null)
        {
            int count = 0;

            Occurences occurenceLevel = index == null ? occurences : occurences[index];

            if (occurenceLevel == null)
                return;
            for (var i = 0; i < occurenceLevel.InnerOccurences.Length; i++)
            {
                if (occurenceLevel.InnerOccurences[i] == null)
                {
                    continue;
                }
                count += occurenceLevel.InnerOccurences[i].Count;
            }
            for (var i = 0; i < occurenceLevel.InnerOccurences.Length; i++)
            {
                if (occurenceLevel.InnerOccurences[i] == null)
                {
                    continue;
                }
                occurenceLevel.Probabilities[i] = (float)occurenceLevel.InnerOccurences[i].Count / count;
            }

        }

        private void CountOccurences(string index)
        {
            Regex rgx = new Regex(index);
            var count = rgx.Matches(text).Count;
            occurences[index].Count = count;
        }

        private void CreateIfNotExist(ref Occurences occurences)
        {
            if (occurences == null)
            {
                occurences = new Occurences(alphabet.Count());
            }
        }

        private void CreateIfNotExist(params char[] indices)
        {
            Occurences temp = occurences.InnerOccurences[indices[0].Normalize()];

            for (var i = 1; i < indices.Length; i++)
            {
                if (temp == null)
                {
                    break;
                }
                temp = temp.InnerOccurences[indices[i].Normalize()];
            }
            if (temp == null)
            {
                temp = new Occurences(10);
            }

        }

        void GetTextFromFile(string filename)
        {
            using (StreamReader filestream = new StreamReader(Path.Combine(Pathname, filename)))
            {
                text = filestream.ReadToEnd().ToLower();
            }
        }


        private class Occurences
        {
            public Occurences(int size)
            {
                innerOccurences = new Occurences[size];
                Probabilities = new float[alphabet.Count()];
                Distribution = new float[alphabet.Count()];
            }

            public int Count = 0;

            public float[] Probabilities;
            public float[] Distribution;
            public Occurences[] InnerOccurences
            {
                get => innerOccurences;
                set
                {
                    innerOccurences = value;
                }
            }

            public Occurences this[string exp]
            {
                get
                {
                    Occurences val = innerOccurences[exp[0].Normalize()];
                    for (int i = 1; i < exp.Length; i++)
                    {
                        val = val.innerOccurences?[exp[i].Normalize()];
                    }
                    return val;
                }
                set
                {
                    Occurences val = innerOccurences[exp[0].Normalize()];
                    for (int i = 1; i < exp.Length; i++)
                    {
                        if (val == null)
                        {
                            return;
                        }
                        val = val.InnerOccurences[exp[i].Normalize()];
                    }
                    val = value;
                }
            }
            public Occurences GetIndex(string exp)
            {
                Occurences val = innerOccurences[exp[0].Normalize()];
                for (int i = 1; i < exp.Length; i++)
                {
                    val = val.innerOccurences?[exp[i].Normalize()];
                }
                return val;
            }
            private Occurences[] innerOccurences;
        }
    }
    public static class CharIntExtensions
    {
        public static int Normalize(this char letter)
        {
            return letter >= 'a' ? letter - 'a' : letter - 6;
        }
        public static char Denormalize(this int number)
        {
            return number == 26 ? ' ' : (char)(number + 'a');
        }
    }
}
