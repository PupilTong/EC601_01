using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Data.SqlClient;

namespace WebApplication.Controllers {
    public class Tweets {
        public Tweets(Int64 TweetsId, string tweetsText, string tweetsCreatedTime, string tweetsImgInfo, Int64 tweetsNLPScore) {
            this.TweetsId = TweetsId;
            this.tweetsText = tweetsText;
            this.tweetsCreatedTime = tweetsCreatedTime;
            this.tweetsImgInfo = tweetsImgInfo;
            this.tweetsNLPScore = tweetsNLPScore;
        }
        public Int64 TweetsId { get; set; }
        public string tweetsText {
            get; set;
        }
        public string tweetsCreatedTime { get; set; }
        public string tweetsImgInfo { get; set; }
        public Int64 tweetsNLPScore { get; set; }
    }
    public class Trend {
        public Trend(string Date, string Tag, Int32 Count) {
            this.Date = Date;
            this.Tag = Tag;
            this.Count = Count;
        }
        public string Date { get; set; }
        public string Tag { get; set; }
        public Int32 Count { get; set; }
    }
    class MyClass {

    }
    public class HomeController : Controller {
        private IConfiguration Configuration;
        public HomeController(IConfiguration configuration) {
            Configuration = configuration;
        }
        // GET: Dashboard
        public IActionResult Index(string tag = "emotion") {
            string sql;


            if (tag == "emotion") {
                //reference:https://blog.csdn.net/winfredzen/article/details/72898152
                sql = "SELECT TOP 15 " +
                    "defaultKeywordsSearchStorage.TweetsMediaJson," +
                    "TweetsText,defaultKeywordsSearchStorage.TweetsCreatedTime,TweetsCreater,defaultKeywordsSearchStorage.TweetsId," +
                    "TweetsCreaterUserId,defaultKewordsSearchCVStorage_copy1.Tags,TweetsNLPScore " +
                    "FROM defaultKeywordsSearchStorage INNER JOIN defaultKewordsSearchCVStorage_copy1 ON defaultKeywordsSearchStorage.TweetsId = defaultKewordsSearchCVStorage_copy1.TweetsId " +
                    "ORDER BY defaultKeywordsSearchStorage.TweetsId DESC ";

                ViewBag.TableTitle = new string[] { "TweetsId", "TweetsText", "TweetsCreateTime", "MediaTags", "TweetsNLPScore" };

            }
            else {
                sql = "select TOP 7 TagsDailyCount.[Date] , TagsId.Tag , TagsDailyCount.[Count] from TagsId " +
                    "INNER JOIN TagsDailyCount on TagsDailyCount.TagsId=TagsId.Id WHERE TagsId.Tag = '" + tag +
                    "' ORDER BY DATE DESC ";
                ViewBag.TableTitle = new string[] { "Data", "Tag", "Count", "", "" };
            }


            SqlConnection con = new SqlConnection(Configuration.GetConnectionString("TweetsContext"));
            List<Object> questResult = new List<Object>();
            SqlCommand cmd = new SqlCommand(sql, con);
            con.Open();
            SqlDataReader rdr = cmd.ExecuteReader();
            while (rdr.Read()) {
                if (tag == "emotion") {
                    var t = new Tweets(rdr.GetInt64(4), rdr.GetString(1), rdr.GetDateTime(2).ToString(), rdr.GetString(6), 0);
                    questResult.Add(t);
                }
                else {

                    var t = new Trend(rdr.GetDateTime(0).ToString(), rdr.GetString(1), rdr.GetInt32(2));
                    questResult.Add(t);
                }

            }
            ViewBag.questResult = questResult;

            con.Close();
            ViewData["Tags"] = tag;
            return View();
        }

    }
}